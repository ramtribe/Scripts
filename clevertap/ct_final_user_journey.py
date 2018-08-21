#!/usr/bin/python 

import csv
import sys
import json
import os
import requests
import datetime

email_list = []
account_id = '698-487-R74Z'
passcode = 'WRE-AQX-MTAL'
url = 'https://api.clevertap.com/1/profile.json'
inputfile = 'C:\Users\Ram Asokan\Desktop\Highgard\Scripts\clevertap\input_email_list\emailcsv_clean.csv'


headers = {
    'X-CleverTap-Account-Id': '%s' % account_id,
    'X-CleverTap-Passcode': '%s' % passcode,
    'Content-Type': 'application/json',
}


with open(inputfile, 'r') as emails:
	reader = csv.DictReader(emails)
	for row in reader:
		email_list.append(row)

i = 0
while i < len(email_list):
	params = email_list[i]
	print "\n New Line:"
	print params
	print "\n New Line:"
	post_response = requests.get(url, headers=headers, params=params)
	post_data = post_response.json()
	print post_data
	print "\n New Line:"
	print post_response
	if post_data.get('record') != None:
		if post_data.get('record').get('email') != None:
			email_id = post_data[u"record"][u"email"].encode('utf-8')
			print email_id
		else:
			email_id = "NULL"
			print email_id
	else:
		email_id = "NULL"
		print "No Records found"
	if post_data.get('record') != None:
		if post_data.get('record').get('identity') != None:
			identity = post_data[u"record"][u"identity"]
			print identity
		else:
			identity = "NULL"
			print identity
	else:
		identity = "NULL"
		print "No records found"
	if post_data.get('record') != None:
		if post_data.get('record').get('profileData') != None:
			if post_data.get('record').get('profileData').get('usertype') != None:
				user_type =  post_data[u"record"][u"profileData"][u"usertype"].encode('utf-8')
				print user_type
			else:
				user_type = "NULL"
				print user_type
			if post_data.get('record').get('profileData').get('subscription') != None:
				subscription_stats = post_data[u"record"][u"profileData"][u"subscription"]
				print subscription_stats
			else:
				subscription_stats = "NULL"
				print subscription_stats
		else:
			user_type = "NULL"
			subscription_stats = "NULL"
			print "No records found"
	else:
		print "No records found"
	if post_data.get('record') != None:
		if post_data.get('record').get('events') != None:
			if post_data.get('record').get('events').get('Media - Started') != None:
				media_started = post_data[u"record"][u"events"][u"Media - Started"][u"count"]
				print media_started
			else:
				media_started = "NULL"
				print media_started
			if post_data.get('record').get('events').get('Registered') != None:
				registered = post_data[u"record"][u"events"][u"Registered"][u"count"]
				print registered
			else:
				registered = "NULL"
				print registered
		else:
			media_started = "NULL"
			registered = "NULL"
			print "No records found"
	else:
		print "No records found"
	if post_data.get('record') != None:
		if post_data.get('record').get('events') != None:
			if post_data.get('record').get('events').get('App Launched') != None:
				if post_data.get('record').get('events').get('App Launched').get('count') != None:
					app_launched = post_data[u"record"][u"events"][u"App Launched"][u"count"]
					print app_launched
				else:
					app_launched = "NULL"
					print app_launched
				if post_data.get('record').get('events').get('App Launched').get('first_seen') != None:
					app_launched_first_date = post_data[u"record"][u"events"][u"App Launched"][u"first_seen"]
					app_launched_first_dt = datetime.datetime.fromtimestamp(app_launched_first_date).strftime('%Y-%m-%d')
					print app_launched_first_dt
				else:
					app_launched_first_dt = "NULL"
					print app_launched_first_dt
			else:
				app_launched = "NULL"
				app_launched_first_dt = "NULL"
				print "No records found"
		else:
			app_launched = "NULL"
			app_launched_first_dt = "NULL"
			print "No records found"
	else:
		print "No records found"
	##header = ["email_id", "subscription_stats", "user_type", "media_started", "registered", "app_launched", "identity", "app_launched_first_dt"]
	final_output = [email_id,str(subscription_stats),user_type,str(media_started),str(registered),str(app_launched),str(identity),str(app_launched_first_dt)]
	##print header
	outputfile = os.path.join('C:\Users\Ram Asokan\Desktop\Highgard\Scripts\clevertap\output_list', '%s' %identity+'.csv' )
	print final_output
	with open(outputfile, 'wb') as f:
		writer = csv.writer(f, delimiter=',')
		writer.writerow(final_output)
	i += 1

