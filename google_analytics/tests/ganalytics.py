import os
from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials

import httplib2
import datetime as dt
from oauth2client import client
from oauth2client import file
from oauth2client import tools

# Create logger
from kfit_lib import custom_logger
logger = custom_logger.setup_logger(
    name=__name__, filename='log/ganalytics.log'
)

try:
    SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']
    DISCOVERY_URI = ('https://analyticsreporting.googleapis.com/v4/reports:batchGet')
    KEY_FILE_LOCATION = 'keys/Project-86bbe81b9d73.json'
    SERVICE_ACCOUNT_EMAIL = os.environ['GA_KFIT_EMAIL']
    VIEW_ID = os.environ['GA_KFIT']  # for KFit Production (All Website Data)
except KeyError:
    logger.error('Please check environment variables and retry.')
    raise

class Report():
    # default values
    start = str(dt.date.today() - dt.timedelta(days=13))
    end = str(dt.date.today())
    analytics = None


def generate_dates(start_date, end_date, delta=15):
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


def get_report(view_id, nextPage=''):
    """ Use the Analytics Service Object to query the Analytics Reporting API V4. """
    params = {
        'reportRequests': [
            {
            'pageSize': '10000',
            'pageToken': nextPage,
            'viewId': view_id,
            'dateRanges': [{'startDate': Report.start, 'endDate': Report.end}],
            'metrics': [{'expression': 'ga:sessions'}, {'expression': 'ga:users'}],
            'dimensions': [{'name': 'ga:date'}, {'name': 'ga:country'}],
            'samplingLevel': 'LARGE'
            }
        ]
    }
    return Report.analytics.reports().batchGet(body=params).execute()


def create_array(response):
    """ Parses the Analytics Reporting API V4 response """
    """ Returns array and next-page token (if any) """
    for report in response.get('reports', []):
        columnHeader = report.get('columnHeader', {})
        dimensionHeaders = columnHeader.get('dimensions', [])
        metricHeaders = columnHeader.get('metricHeader', {}).get('metricHeaderEntries', [])
        rows = report.get('data', {}).get('rows', [])
        nextPage = report.get('nextPageToken')

        # Create header for the array
        dim_heads = [str(dim) for dim in dimensionHeaders]
        met_heads = [str(metric['name']) for metric in metricHeaders]
        header_row = [[head.replace('ga:', '') for head in (dim_heads + met_heads)]]

        newArray = []
        for row in rows:
            dimensions = row.get('dimensions', [])
            dateRangeValues = row.get('metrics', [])

            newRow = []
            for header, dimension in zip(dimensionHeaders, dimensions):
                newRow.append(dimension.encode('utf-8'))

            for i, values in enumerate(dateRangeValues):
                for metricHeader, value in zip(metricHeaders, values.get('values')):
                    newRow.append(str(value))

            newArray.append(newRow)
        return header_row, newArray, nextPage # [[header_row]], [[nextPage]]


def process(view_id):
    """ Download remaining pages if any """
    response = get_report(view_id)
    header, array, next_page = create_array(response)
    if next_page == None:
        pass
    else:
        while next_page != None:
            logger.info('Google Analytics has a limit of 10,000 rows per API query, performing next query from row {}...'.format(int(next_page)+1))
            newResponse = get_report(VIEW_ID, next_page)
            header, newArray, next_page = create_array(newResponse)
            array += newArray
    logger.info('Downloaded {} rows.'.format(len(array)))
    return header, array # Includes header


def download_by_batches(view_id, start_date, end_date):
    """ Separates query date range into smaller ranges for higher precision """
    # Generate date ranges to iterate
    date_ranges = [date for date in generate_dates(start_date, end_date)]
    num_batches = len(date_ranges)

    if num_batches > 1:
        logger.info('Query will be split into {} batches.'.format(num_batches))
    
    # Initiate download by date ranges
    batch = 1
    combined_array = []
    for start, end in date_ranges:
        # Set date range
        Report.start = start
        Report.end = end

        logger.info('Batch {}/{}: {} to {}'.format(batch, num_batches, start, end))
        header, array = process(view_id)
        if len(array) > 0:
            combined_array.extend(array)
        batch += 1

    return header + combined_array


def main(start_date, end_date):
    logger.info('Running ganalytics.py for KFit..')
    logger.info('Downloading data from {} until {}..'.format(start_date, end_date))
    Report.analytics = initialize_analyticsreporting()
    return download_by_batches(VIEW_ID, start_date, end_date) # Include header


if __name__ == '__main__':
    arr = main('2015-03-01', 'today')
    import csv
    with open('temp/ganalytics.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerows(arr)
        