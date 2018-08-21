#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function

__author__ = 'ram@tribenow.tv (Ram Asokan)'

import argparse
import sys
import csv
import json
import psycopg2 as pg
import os


from pprint import pprint
from googleapiclient.errors import HttpError
from googleapiclient import sample_tools
from oauth2client.client import AccessTokenRefreshError

fileOutput = os.path.join('C:\Users\Ram Asokan\Desktop\Highgard\Scripts\google_analytics','ga_view_imps.csv')
db_conn_para = "dbname='tribe_staging_v21' user='sa' host='localhost' " + \
				"password='9FhkQsWRmRbNeWDUjgC7'"

def main(argv):
  # Authenticate and construct service.
  service, flags = sample_tools.init(
      argv, 'analytics', 'v3', __doc__, __file__,
      scope='https://www.googleapis.com/auth/analytics.readonly')

  # Try to make a request to the API. Print the results or handle errors.
  try:
    first_profile_id = get_profile_id(service)
    if not first_profile_id:
      print('Could not find a valid profile for this user.')
    else:
		results = get_video_imps(service, first_profile_id)
		get_results(results)
		pg_conn()
		
  except TypeError as error:
    # Handle errors in constructing a query.
    print(('There was an error in constructing your query : %s' % error))

  except HttpError as error:
    # Handle API errors.
    print(('Arg, there was an API error : %s : %s' %
           (error.resp.status, error._get_reason())))

  except AccessTokenRefreshError:
    # Handle Auth errors.
    print ('The credentials have been revoked or expired, please re-run '
           'the application to re-authorize')


def get_profile_id(service):
  """Traverses Management API to return the first profile id.

  This first queries the Accounts collection to get the first account ID.
  This ID is used to query the Webproperties collection to retrieve the first
  webproperty ID. And both account and webproperty IDs are used to query the
  Profile collection to get the first profile id.

  Args:
    service: The service object built by the Google API Python client library.

  Returns:
    A string with the first profile ID. None if a user does not have any
    accounts, webproperties, or profiles.
  """

  accounts = service.management().accounts().list().execute()

  #Tribe Account ID
  webproperties = service.management().webproperties().list(accountId='70244335').execute()
  #Tribe App Property ID
  profiles = service.management().profiles().list(accountId='70244335',webPropertyId='UA-70244335-1').execute()
  #Tribe App Indonesia View
  return profiles.get('items')[2].get('id')
  return None

def get_video_imps(service, profile_id):
  """Executes and returns data from the Core Reporting API.

  This queries the API for the top 25 organic search terms by visits.

  Args:
    service: The service object built by the Google API Python client library.
    profile_id: String The profile ID from which to retrieve analytics data.

  Returns:
    The response returned from the Core Reporting API.
  """

  return service.data().ga().get(
      ids='ga:' + profile_id,
      start_date='7daysAgo',
      end_date='yesterday',
      metrics='ga:totalEvents',
      dimensions='ga:date,ga:country,ga:dimension2,ga:dimension3,ga:eventAction',
      sort='ga:country,ga:date',
      filters='ga:eventAction=~Asset;ga:country==Indonesia,ga:country==Philippines',
      start_index='1',
      max_results='10000').execute()


def get_results(results):
  """Prints out the results.

  This prints out the profile name, the column headers, and all the rows of
  data.

  Args:
    results: The response returned from the Core Reporting API.
  """

  print()
  print('Profile Name: %s' % results.get('profileInfo').get('profileName'))
  print()

  outputFile = open(fileOutput, 'wb')
  
  # Print header.
  output = []
  for header in results.get('columnHeaders', {}):
	output.append(header.get('name'))
  final_output = csv.writer(outputFile, delimiter='^')
  final_output.writerow(output)


  # Print data table.
  if results.get('rows', []):
    for row in results.get('rows'):
      output = []
      for cell in row:
		output.append(cell.encode('utf-8'))
      if any(field.strip() for field in output):
	    final_output.writerow(output)
  else:
    print('No Rows Found')
	
  outputFile.close()

def pg_conn():
  conn = None
  try:
	conn = pg.connect(db_conn_para)
	cursor = conn.cursor()
	with open(fileOutput, 'r') as f:
		cursor.copy_from(f, 'ga_view_impressions', sep='^')
	conn.commit()
  except (Exception, pg.DatabaseError) as error:
	print(error)
  finally:
	if conn is not None:
		conn.close()
	
  f.close()	
  

if __name__ == '__main__':
  main(sys.argv)
