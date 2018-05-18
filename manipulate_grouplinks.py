#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import csv
import re
import json
import requests
import unicodedata
from shutil import copy
from bs4 import BeautifulSoup


# Create trust_list - a list of dictionaries, with one per trust. Add trusts that don't already feature in the list, and iterate the number of schools where they do
trust_list=[]
companies_house_url_stub='https://beta.companieshouse.gov.uk/company/'

github_url="https://github.com/philipnye/ainfo/tree/master/data"
github_raw_url="https://raw.githubusercontent.com/philipnye/ainfo/master/data/"

html=requests.get(github_url).text
soup=BeautifulSoup(html, 'html.parser')
for a in soup.find_all('a'):
    if str(a.get('title')).endswith('csv'):     # tag.get('attr') in Beautiful Soup acts like a Python dictionary, returning None where attr is undefined.
        file_name=str(a.get('title'))
        file_url=github_raw_url+file_name        # expectation is that there is one and only data file
csv_file=requests.get(file_url)
csv_file=csv_file.iter_lines()      # is required in order for csv file to be read correctly, without errors caused by new-line characters
reader=csv.DictReader(csv_file)
for row in reader:
	if row['Group Type'] in ('Multi-academy trust','Single-academy trust'):
		trust_code=row['Linked UID']
		trust_name=row['Group Name']
		trust_name=trust_name.replace('\xa0', ' ')		# replace characters that will prevent saving as JSON
		trust_name=trust_name.replace('\x92', '\'')
		trust_name=trust_name.replace('\xc9', 'E')
		# trust_name=trust_name.decode('windows-1252')
		# trust_name=trust_name.decode('windows-1252').encode('utf-8', 'ignore')
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

with open('trusts.json', 'w') as out_file:
    json.dump(trust_list, out_file)


# Create a folder for each trust with a copy of template page
path_stub='C:/Users/pn/Documents/Work/Coding/GitHub/ainfo/web/'

for trust in trust_list:
	if trust['trust_name'].lower()[0]=='a':
		path=path_stub+trust['trust_code']
		file_name=trust['trust_name_simple'].lower()+'.html'
		if not os.path.exists(path):
			os.makedirs(path)
		file_path=os.path.join(path, file_name)		# done outside the if not statement, as we want a fresh copy of the template in each case
		copy('C:/Users/pn/Documents/Work/Coding/GitHub/ainfo/template.html', file_path)
		with open(file_path) as read_file:
			html=read_file.read()
		soup=BeautifulSoup(html, 'html.parser')
		new_h1=soup.new_tag('h1')
		new_h1.string=trust['trust_name']
		soup.body.append(new_h1)
		with open(file_path, 'w') as write_file:
		    write_file.write(str(soup))


# Sort trust_list
trust_list=sorted(trust_list, key=lambda k:k['trust_name']) 


# Generate ainfo index.html
dir=('C:/Users/pn/Documents/Work/Coding/GitHub/ainfo')
os.chdir(dir)

base_url='https://philipnye.github.io/ainfo/web/'

with open('template.html') as read_file:
	html=read_file.read()
soup=BeautifulSoup(html, 'html.parser')
for trust in trust_list:
	if trust['trust_name'].lower()[0]=='a':
		trust_page_url=base_url+trust['trust_code']+'/'+trust['trust_name_simple'].lower()
		new_tag=soup.new_tag('a', href=trust_page_url)
		new_tag.string=trust['trust_name']
		soup.body.append(new_tag)
		line_break=soup.new_tag('br')
		soup.body.append(line_break)
with open('index.html', 'w') as write_file:
    write_file.write(str(soup))
