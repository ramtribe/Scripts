#!/usr/bin/python

import json
import csv
import sys
import os
import pandas as pd
from pandas.io.json import json_normalize
import psycopg2 as pg

## Declare variables
data = []
fileInput = 'C:\Users\Ram Asokan\Desktop\Highgard\Scripts\wranglings\dumps\example_1.json'
fileOutput = os.path.join('C:\Users\Ram Asokan\Desktop\Highgard\Scripts\wranglings\dumps', 'test.csv')
db_conn_para = "dbname='tribe_staging_v21' user='sa' host='localhost' " + \
				"password='9FhkQsWRmRbNeWDUjgC7'"

## Test - View Open .json file
with open(fileInput) as f:
	data = json.load(f)

## View .json data
print json.dumps(data, indent=4, sort_keys=False) 
print("\n")

## Tabulate data 
datafile = json_normalize(data)

## Test - View .json file
print(datafile)
print("\n")

## Load .json data to .csv
datafile.to_csv(fileOutput, index=None)

## Load .csv to db
conn = None			
try:			
	conn = pg.connect(db_conn_para)
	cursor = conn.cursor()
	cursor.execute("SELECT * FROM public.users limit 5;")
	rows = cursor.fetchall()	
	print(rows)
	print("\n")
except (Exception, pg.DatabaseError) as error:
	print(error)
finally:
	if conn is not None:
		conn.close()
	
## Close files
f.close()