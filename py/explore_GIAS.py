#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import csv
import re
import datetime
import json
import requests
import unicodedata
from shutil import copy
from bs4 import BeautifulSoup
from bs4 import NavigableString

# Create trust_list - a list of dictionaries, with one per trust. Add trusts that don't already feature in the list, and iterate the number of schools where they do
total_list=[]
trust_list=[]
school_list=[]
gias_url_stub='https://get-information-schools.service.gov.uk/Establishments/Establishment/Details/'
companies_house_url_stub='https://beta.companieshouse.gov.uk/company/'

os.chdir(os.path.dirname( __file__ ))
os.chdir('..')
os.chdir('data')

for source_file in os.listdir('.'):
	if source_file.endswith('.csv') and source_file[:14]=='edubasealldata':
		with open(source_file, 'rb') as infile:
			reader=csv.DictReader(infile)
			found=False
			for row in reader:
				if row['SchoolSponsors (name)']=='This is a co-sponsored academy. Details of the sponsors of co-sponsored academies are not included in the current version of performance tables but this information will be available early in 2016':
					found=True
			if found==True:
				print source_file
