#!/usr/bin/python
# -*- coding: utf-8 -*-

import pymongo
from pymongo import MongoClient
import json
import csv
import pprint
import sys
import pandas as pd
from pandas.io.json import json_normalize

client = MongoClient('mongodb://user8e8ebe:3aa15fDmuMaVA9aa795@cluster-pgrs2000-0-ap-northeast-1-scalabledbs.cloudstrap.io:30000,cluster-pgrs2000-1-ap-northeast-1-scalabledbs.cloudstrap.io:30000,cluster-pgrs2000-2-ap-northeast-1-scalabledbs.cloudstrap.io:30000/pg-app-1-jp-jvjpaykbk2qyvtye0kx475yj8d23bi?replicaSet=pgrs2000&ssl=true')
db = client['pg-app-1-jp-jvjpaykbk2qyvtye0kx475yj8d23bi']
errorScreens = db['errorScreens']

pprint.pprint(errorScreens.count())
print("\n")

pprint.pprint(errorScreens.find_one())
print("\n")

datafile = json_normalize(errorScreens.find_one())

##for errorScreens in errorScreens.find():
	##pprint.pprint(errorScreenss)	



