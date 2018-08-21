from __future__ import print_function # Python 2/3 compatibility
import os
import glob
import httplib2
import datetime as dt
import re
import csv
from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
from oauth2client import client
from oauth2client import file
from oauth2client import tools

# Create logger
from kfit_lib import custom_logger
logger = custom_logger.setup_logger(
    name=__name__, filename='log/ganalytics_groupon.log'
)

try:
    SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']
    DISCOVERY_URI = ('https://analyticsreporting.googleapis.com/v4/reports:batchGet')
    KEY_FILE_LOCATION = 'keys/Project-eaebb2f6d1c4.json'
    SERVICE_ACCOUNT_EMAIL = os.environ['GA_ID_EMAIL']
    DESKTOP_VIEW_ID = os.environ['GA_ID_DESKTOP'] # Desktop web data
    MOBILE_VIEW_ID = os.environ['GA_ID_MOBILE'] # Mobile web data
except KeyError as e:
    logger.exception('Please check environment variables and retry.')
    raise


def check_dir():
    """Prepare temporary directory for ga_groupon."""
    if os.path.isdir('temp/ga'):
        existing_files = glob.glob('temp/ga/ga_groupon_*.csv')
        logger.info('Removing existing files...')
        [os.remove(f) for f in existing_files]
    else:
        os.makedirs('temp/ga')


class Report():
    # default values
    # start = str(dt.date.today() - dt.timedelta(days=13))
    # end = str(dt.date.today())
    analytics = None


def generate_dates(start_date, end_date, delta=6):
    """ Generate batched date ranges to retrieve more accurate results """
    """ Returns [[date, date], [date,date], etc] """
    def format_date(date):
        return dt.datetime.strftime(date, '%Y-%m-%d')

    start = dt.datetime.strptime(start_date, '%Y-%m-%d')
    end = dt.datetime.strptime(end_date, '%Y-%m-%d')

    current = start
    while current <= end:
        new = current + dt.timedelta(days=delta)
        if new <= end:
            yield [format_date(current), format_date(new)]
        else:
            yield [format_date(current), format_date(end)]
        current += dt.timedelta(days=delta+1)


def initialize_analyticsreporting():
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
                    KEY_FILE_LOCATION, scopes=SCOPES)
    http = credentials.authorize(httplib2.Http())

    # Build the service object.
    analytics = build('analytics', 'v4', http=http, discoveryServiceUrl=DISCOVERY_URI)
    return analytics


def get_report(view_id, report_type, start_date, end_date, nextPage=''):
    """Query GA based on desired report type."""
    # Store custom report parameters
    reports = {
        # Report 1
        'site_performance_aggregates': {
            'metrics': [
                {'expression': 'ga:users'}, 
                {'expression': 'ga:newUsers'},
                {'expression': 'ga:sessions'}, 
                {'expression': 'ga:pageviews'},
                {'expression': 'ga:organicSearches'},
                {'expression': 'ga:transactions'},
                {'expression': 'ga:transactionRevenue'}
            ],
            'dimensions': [{'name': 'ga:date'}]
        },
        # Report 2
        'site_performance_breakdown': {
            'metrics': [
                {'expression': 'ga:users'}, 
                {'expression': 'ga:newUsers'},
                {'expression': 'ga:sessions'}, 
                {'expression': 'ga:pageviews'},
                {'expression': 'ga:organicSearches'},
                {'expression': 'ga:transactions'},
                {'expression': 'ga:transactionRevenue'}
            ],
            'dimensions': [
                {'name': 'ga:date'},
                {'name': 'ga:country'},
                {'name': 'ga:sourceMedium'},
                {'name': 'ga:campaign'},
                {'name': 'ga:userType'}
            ]
        },
        # Report 3
        'page_tracking': {
            'metrics': [
                {'expression': 'ga:pageviews'}, 
                {'expression': 'ga:uniquePageviews'},
                {'expression': 'ga:avgTimeOnPage'},
                {'expression': 'ga:entrances'},
                {'expression': 'ga:exits'}
            ],
            'dimensions': [
                {'name': 'ga:date'}, 
                {'name': 'ga:hostname'},
                {'name': 'ga:pagePath'},
                {'name': 'ga:pageTitle'},
            ]           
        }
    }

    # Shared/Default report parameters
    params = {
        'reportRequests': [{
            'pageSize': '10000',
            'pageToken': nextPage,
            'viewId': view_id,
            'dateRanges': [{'startDate': start_date, 'endDate': end_date}],
            'metrics': reports.get(report_type).get('metrics'),
            'dimensions': reports.get(report_type).get('dimensions')
        }]
    }   
    return Report.analytics.reports().batchGet(body=params).execute()    


def parse_pagepath(val):
    """Get page_path category, and extract deal_id if any.
    Returns: ['category', 'deal_id']"""
    deal_id = None
    if ('/promo.php?' in val) and ('/product/' not in val):
        category = 'deal_views'
        # Search for '.php?id=000'' or '.php?i=000'
        results = re.search(r".php\?i(d|)=\d+", val)
        if results != None:
            res = results.group(0)
            # Extract deal_id
            deal_id = res.replace('d', '').replace('.php?i=', '')
    elif ('/voucher/' in val):
        if ('voucher/?e=' in val):
            category = 'others'
        elif re.search(r"/\d+", val) == None: # '/000'
            category = 'others'
        else:
            category = 'deal_views'
            results = re.search(r"/\d+", val) # '/000'
            if results != None:
                deal_id = results.group(0).replace('/', '')
    elif ('/purchase.php?' in val):
        category = 'option_selection_page'
        results = re.search(r".php\?id=\d+", val) # '.php?id=000'
        if results != None:
            deal_id = results.group(0).replace('.php?id=', '')
    elif ('/payment-form.php' in val) or ('/confirm.php' in val):
        category = 'payment_confirmation'
    elif ('/purchase-success.php?' in val):
        category = 'payment_success'
    else:
        category = 'others'
    return [category, deal_id]


def create_array(response, view_id):
    """ Parses the Analytics Reporting API V4 response """
    """ Returns array and next-page token (if any) """
    if view_id == MOBILE_VIEW_ID:
        row_tag = 'Mobile'
    elif view_id == DESKTOP_VIEW_ID:
        row_tag = 'Desktop'

    for report in response.get('reports', []):
        columnHeader = report.get('columnHeader', {})
        dimensionHeaders = columnHeader.get('dimensions', [])
        metricHeaders = columnHeader.get('metricHeader', {}).get('metricHeaderEntries', [])
        rows = report.get('data', {}).get('rows', [])
        nextPage = report.get('nextPageToken')

        # Create header for the array
        dim_heads = [str(dim) for dim in dimensionHeaders]
        met_heads = [str(metric['name']) for metric in metricHeaders]
        header_row = [['web_type'] + [head.replace('ga:', '') for head in (dim_heads + met_heads)]]

        newArray = []
        for row in rows:
            dimensions = row.get('dimensions', [])
            dateRangeValues = row.get('metrics', [])

            newRow = [row_tag] # Prefix row with Desktop or Mobile
            for header, dimension in zip(dimensionHeaders, dimensions):
                newRow.append(dimension.encode('utf-8'))

            for i, values in enumerate(dateRangeValues):
                for metricHeader, value in zip(metricHeaders, values.get('values')):
                    newRow.append(str(value))

            newArray.append(newRow)
        return header_row, newArray, nextPage


def save_csv(array, view_id, report_type, batch):
    """Write array to CSV."""
    if view_id == MOBILE_VIEW_ID:
        tag = 'Mobile'
    elif view_id == DESKTOP_VIEW_ID:
        tag = 'Desktop'
    filename = 'temp/ga/ga_groupon_{}_{}_{}.csv'.format(tag, report_type, batch)
    with open(filename, 'w') as o:
        csv.writer(o).writerows(array)


def process(view_id, report_type, start_date, end_date):
    """ Download remaining pages if any """
    response = get_report(view_id, report_type, start_date, end_date)
    header, array, next_page = create_array(response, view_id)
    if next_page == None:
        pass
    else:
        while next_page != None:
            logger.info('Google Analytics has a limit of 10,000 rows per API query, '
            'performing next query from row {}...'.format(int(next_page)+1))
            newResponse = get_report(
                view_id, report_type, start_date, end_date, nextPage=next_page)
            header, newArray, next_page = create_array(newResponse, view_id)
            array += newArray
    logger.info('Downloaded {} rows.'.format(len(array)))
    return header, array # Includes headers


def download_by_batches(report_type, view_id, start_date, end_date, delta=6):
    """ Separates query date range into smaller ranges for higher precision """
    # Generate date ranges to iterate
    date_ranges = [date for date in generate_dates(start_date, end_date, delta=delta)]
    num_batches = len(date_ranges)

    if num_batches > 1:
        logger.info('Query will be split into {} batches.'.format(num_batches))
    
    # Initiate download by date ranges
    batch = 1
    # combined_array = []
    for start, end in date_ranges:
        logger.info('Batch {}/{}: {} to {}'.format(batch, num_batches, start, end))
        header, array = process(view_id, report_type, start, end)
        if len(array) > 0:
            # Add calculated columns for 'page_tracking' report_type
            if report_type == 'page_tracking':
                [row.extend(parse_pagepath(row[3])) for row in array]
                # Fix 'pagePath' and 'pageTitle' field
                for row in array:
                    row[3] = row[3].replace('\\', '')
                    row[4] = row[4].replace('\\', '')
            save_csv(header + array, view_id, report_type, batch)
        batch += 1


def main(report_type, start_date, end_date):
    """Writes both Desktop and Mobile report queries into file.
    
    Args:
        report_type:
            Specify either 'site_performance_aggregates',
            'site_performance_breakdown' or 'page_tracking'.
        start_date: Date from which to query.
        end_date: Date until which to query.
    Outputs:
        CSV report file
    """

    logger.info('Running ganalytics_groupon.py for Groupon ID..')
    check_dir()
    logger.info('Downloading data from {} until {}..'.format(start_date, end_date))
    Report.analytics = initialize_analyticsreporting()

    # Use appropriate time delta for report_type
    time_delta = {
        'site_performance_aggregates': 365,
        'site_performance_breakdown': 6,
        'page_tracking': 1
    }

    # Query according to report_type
    logger.info('\nQuerying Groupon Desktop Web...')
    download_by_batches(
        report_type, DESKTOP_VIEW_ID, 
        start_date, end_date, delta=time_delta[report_type])

    logger.info('\nQuerying Groupon Mobile Web...')
    download_by_batches(
        report_type, MOBILE_VIEW_ID, 
        start_date, end_date, delta=time_delta[report_type])


if __name__ == '__main__':
    main('site_performance_aggregates', '2016-10-01', '2016-10-17')
    # main('site_performance_breakdown', '2016-10-01', '2016-10-17')
    # main('page_tracking', '2016-10-01', '2016-10-17')
