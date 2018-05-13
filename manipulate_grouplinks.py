#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import csv
import re
import json
import unicodedata
from shutil import copy

# Create trust_list - a list of dictionaries, with one per trust. Add trusts that don't already feature in the list, and iterate the number of schools where they do
trust_list=[]
companies_house_url_stub='https://beta.companieshouse.gov.uk/company/'

dir=('C:/Users/pn/Dropbox/Unedited EduBase data')
os.chdir(dir)

with open('grouplinks_edubaseallacademiesandfree20161216.csv', 'rb') as infile:
	reader = csv.DictReader(infile)
	for row in reader:
		if row['Group Type'] in ('Multi-academy trust','Single-academy trust'):
			trust_code=row['Linked UID']
			trust_name=row['Group Name']
			trust_name=trust_name.replace('\xa0', ' ')		# replace characters that will prevent saving as JSON
			trust_name=trust_name.replace('\x92', '\'')
			# trust_name=trust_name.decode("windows-1252")
			# trust_name=trust_name.decode("windows-1252").encode('utf-8', 'ignore')
			# print trust_name
			trust_type=row['Group Type']
			companies_house_number=row['Companies House Number']
			if any(dict['trust_code'] == trust_code for dict in trust_list)==True:
				for dict in trust_list:
					if dict['trust_code']==trust_code:
						dict['school_count']=dict['school_count']+1
						break
			else:
				trust_name_simple=re.sub('[^a-zA-Z0-9 \-\.@]', '', trust_name)
				trust_name_simple=trust_name_simple.replace (' ', '-')
				trust_name_simple=trust_name_simple.replace ('--', '-')
				trust_list.append({'trust_code':trust_code, 'trust_name':trust_name, 'trust_name_simple':trust_name_simple, 'trust_type':trust_type,'companies_house_number':companies_house_number,'companies_house_url':companies_house_url_stub+companies_house_number,'school_count':1})

dir=('C:/Users/pn/Documents/Work/Coding/GitHub/ainfo/data')
os.chdir(dir)

with open('trusts.json', 'w') as outfile:
    json.dump(trust_list, outfile)


# Create a folder for each trust with a copy of template page
path_stub='C:/Users/pn/Documents/Work/Coding/GitHub/ainfo/web/'

for trust in trust_list:
	path=path_stub+trust['trust_code']
	file_name=trust['trust_name_simple']+'.html'
	if not os.path.exists(path):
		os.makedirs(path)
	copy('C:/Users/pn/Documents/Work/Coding/GitHub/ainfo/template.html', os.path.join(path, file_name))		# done outside the if not statement, as we want a fresh copy of the template in each case
