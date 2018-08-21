"""Script to pull data from Google Analytics for Fave Web."""

from kfit_lib import google_analytics as ga
import datetime as dt
import argparse
import csv
import os

# Create logger
from kfit_lib import custom_logger
logger = custom_logger.setup_logger(
    name=__name__, filename='log/ga_fave.log'
)

try:
    KEY_FILE_LOCATION = 'keys/Project-eaebb2f6d1c4.json'
    SERVICE_ACCOUNT_EMAIL = os.environ['GA_FAVE_EMAIL']
    VIEW_ID = os.environ['GA_FAVE']  # for Fave Production (All Website Data)
except KeyError:
    logger.error('Please check environment variables and retry.')
    raise


def signup_flow(start_date, end_date):
    analytics = ga.Reporting(SERVICE_ACCOUNT_EMAIL, KEY_FILE_LOCATION)
    request_params = {
        'viewId': VIEW_ID,
        'dateRanges': [{'startDate': start_date, 'endDate': end_date}],
        'metrics': [
            {'expression': 'ga:totalEvents'}, 
            {'expression': 'ga:uniqueEvents'}
        ],
        'dimensions': [
            {'name': 'ga:date'}, 
            {'name': 'ga:country'},
            {'name': 'ga:eventCategory'}, 
            {'name': 'ga:eventAction'}
        ],
        'dimensionFilterClauses': [
            {
                'filters': [
                    {
                        'dimensionName': 'ga:eventCategory',
                        'operator': 'EXACT',
                        'expressions': ['Sign Up']
                    }
                ]
            }
        ]
    }
    array = analytics.request(request_params, split_date_range=True)
    with open('temp/ga_fave_signupflow.csv', 'w') as o:
        csv.writer(o).writerows(array)


def traffic_report(start_date, end_date):
    analytics = ga.Reporting(SERVICE_ACCOUNT_EMAIL, KEY_FILE_LOCATION)
    request_params = {
        'viewId': VIEW_ID,
        'dateRanges': [{'startDate': start_date, 'endDate': end_date}],
        'metrics': [
            {'expression': 'ga:users'}, 
            {'expression': 'ga:newUsers'}, 
            {'expression': 'ga:sessions'}, 
            {'expression': 'ga:pageviews'}, 
            {'expression': 'ga:uniquePageviews'}, 
            {'expression': 'ga:bounceRate'},
            {'expression': 'ga:timeOnPage'},
            {'expression': 'ga:sessionDuration'}
        ],
        'dimensions': [
            {'name': 'ga:date'}, 
            {'name': 'ga:country'},
            {'name': 'ga:deviceCategory'}
        ]
    }
    array = analytics.request(request_params, split_date_range=True)
    with open('temp/ga_fave_traffic.csv', 'w') as o:
        csv.writer(o).writerows(array)


def active_users(start_date, end_date):
    analytics = ga.Reporting(SERVICE_ACCOUNT_EMAIL, KEY_FILE_LOCATION)
    request_params = {
        'viewId': VIEW_ID,
        'dateRanges': [{'startDate': start_date, 'endDate': end_date}],
        'metrics': [
            # {'expression': 'ga:1dayUsers'}, 
            # {'expression': 'ga:7dayUsers'}, 
            # {'expression': 'ga:14dayUsers'}, 
            {'expression': 'ga:30dayUsers'}, 
        ],
        'dimensions': [
            {'name': 'ga:date'}
        ]
    }
    array = analytics.request(request_params, split_date_range=True)
    with open('temp/ga_fave_active_users.csv', 'w') as o:
        csv.writer(o).writerows(array)


def fave_page_tracking(start_date, end_date):
    analytics = ga.Reporting(
        SERVICE_ACCOUNT_EMAIL, KEY_FILE_LOCATION, delta=0
    )
    request_params = {
        'viewId': VIEW_ID,
        'dateRanges': [{'startDate': start_date, 'endDate': end_date}],
        'metrics': [
            {'expression': 'ga:pageviews'}, 
            {'expression': 'ga:uniquePageviews'},
            {'expression': 'ga:timeOnPage'},
            {'expression': 'ga:avgTimeOnPage'},
            {'expression': 'ga:entrances'},
            {'expression': 'ga:exits'}
        ],
        'dimensions': [
            {'name': 'ga:date'}, 
            {'name': 'ga:country'},
            {'name': 'ga:hostname'},
            {'name': 'ga:previousPagePath'},
            {'name': 'ga:pagePath'},
            {'name': 'ga:pageTitle'},
        ],
        'dimensionFilterClauses': [
            {
                'filters': [
                    {
                        'dimensionName': 'ga:country',
                        'operator': 'IN_LIST',
                        'expressions': ['Malaysia', 'Indonesia', 'Singapore']
                    }
                ]
            }
        ]
    }

    # Dump response in batches to reduce memory usage
    analytics.request(
        request_params, 
        split_date_range=True,
        output_file='temp/ga_fave_page_tracking.csv'
    )


def fave_events(start_date, end_date):
    analytics = ga.Reporting(SERVICE_ACCOUNT_EMAIL, KEY_FILE_LOCATION)
    request_params = {
        'viewId': VIEW_ID,
        'dateRanges': [{'startDate': start_date, 'endDate': end_date}],
        'metrics': [
            {'expression': 'ga:totalEvents'}, 
            {'expression': 'ga:uniqueEvents'}
        ],
        'dimensions': [
            {'name': 'ga:date'}, 
            {'name': 'ga:country'},
            {'name': 'ga:deviceCategory'},
            {'name': 'ga:eventCategory'}, 
            {'name': 'ga:eventAction'}
        ]
    }
    array = analytics.request(request_params, split_date_range=True)
    with open('temp/ga_fave_events.csv', 'w') as o:
        csv.writer(o).writerows(array)


def fave_transaction_tracking(start_date, end_date):
    analytics = ga.Reporting(
        SERVICE_ACCOUNT_EMAIL, KEY_FILE_LOCATION, delta=15
    )
    request_params = {
        'viewId': VIEW_ID,
        'dateRanges': [{'startDate': start_date, 'endDate': end_date}],
        'metrics': [
            {'expression': 'ga:itemQuantity'}, 
            {'expression': 'ga:transactionRevenue'}, 
            {'expression': 'ga:itemRevenue'}, 
        ],
        'dimensions': [
            {'name': 'ga:date'},
            {'name': 'ga:transactionId'},
            {'name': 'ga:country'},
            {'name': 'ga:medium'},
            {'name': 'ga:source'},
            {'name': 'ga:campaign'},
        ]
    }
    array = analytics.request(request_params, split_date_range=True)
    with open('temp/ga_fave_transaction_tracking.csv', 'w') as o:
        csv.writer(o).writerows(array)


def fave_traffic_source(start_date, end_date):
    analytics = ga.Reporting(
        SERVICE_ACCOUNT_EMAIL, KEY_FILE_LOCATION, delta=15
    )
    request_params = {
        'viewId': VIEW_ID,
        'dateRanges': [{'startDate': start_date, 'endDate': end_date}],
        'metrics': [
            {'expression': 'ga:users'}, 
            {'expression': 'ga:newUsers'}, 
            {'expression': 'ga:sessions'}, 
            {'expression': 'ga:pageviews'}, 
            {'expression': 'ga:uniquePageviews'}, 
        ],
        'dimensions': [
            {'name': 'ga:date'},
            {'name': 'ga:country'}, 
            {'name': 'ga:deviceCategory'},
            {'name': 'ga:medium'},
            {'name': 'ga:source'},
            {'name': 'ga:campaign'},
            {'name': 'ga:keyword'},
        ],
    }
    array = analytics.request(request_params, split_date_range=True)
    with open('temp/ga_fave_traffic_source.csv', 'w') as o:
        csv.writer(o).writerows(array)


if __name__ == '__main__':
    traffic_report('2017-01-01', '2017-01-31')
