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
from bs4 import NavigableString


# Create trust_list - a list of dictionaries, with one per trust. Add trusts that don't already feature in the list, and iterate the number of schools where they do
trust_list=[]
companies_house_url_stub='https://beta.companieshouse.gov.uk/company/'

github_url='https://github.com/philipnye/ainfo/tree/master/data'
github_raw_url='https://raw.githubusercontent.com/philipnye/ainfo/master/data/'

estab_type_count={
	'sponsored_academy_count':None,
	'converter_academy_count':None,
	'free_school_count':None,
	'utc_studio_school_count':None
}

html=requests.get(github_url).text
soup=BeautifulSoup(html, 'html.parser')
for a in soup.find_all('a'):
	if str(a.get('title')).endswith('csv'):	 # tag.get('attr') in Beautiful Soup acts like a Python dictionary, returning None where attr is undefined.
		file_name=str(a.get('title'))
		file_url=github_raw_url+file_name		# expectation is that there is one and only data file
csv_file=requests.get(file_url)
csv_file=csv_file.iter_lines()	  # is required in order for csv file to be read correctly, without errors caused by new-line characters
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
		trust_type=row['Group Type']
		companies_house_number=row['Companies House Number']
		estab_type_count=dict.fromkeys(estab_type_count, 0)
		if row['TypeOfEstablishment (name)'] in ('Academy sponsor led','Academy alternative provision sponsor led','Academy special sponsor led','Academy 16 to 19 sponsor led'):
			 estab_type_count['sponsored_academy_count']=1
		elif row['TypeOfEstablishment (name)'] in ('Academy converter','Academy alternative provision converter','Academy special converter','Academy 16-19 converter'):
			 estab_type_count['converter_academy_count']=1
		elif row['TypeOfEstablishment (name)'] in ('Free schools','Free schools alternative provision','Free schools special','Free schools 16 to 19'):
			 estab_type_count['free_school_count']=1
		elif row['TypeOfEstablishment (name)'] in ('University technical college','Studio schools'):
			 estab_type_count['utc_studio_school_count']=1
		if row['PhaseOfEducation (name)'] in ('Primary','Middle deemed primary'):
			 estab_phase='Primary'
		elif row['PhaseOfEducation (name)'] in ('Secondary','Middle deemed secondary'):
			 estab_phase='Secondary'
		elif row['PhaseOfEducation (name)'] in ('All through'):
			 estab_phase='All-through'
		elif row['PhaseOfEducation (name)'] in ('Not applicable') and row['TypeOfEstablishment (name)'] in ('Academy alternative provision converter','Academy alternative provision sponsor led'):
			 estab_phase='Alternative provision'
		elif row['PhaseOfEducation (name)'] in ('Not applicable') and row['TypeOfEstablishment (name)'] in ('Academy special converter','Academy special sponsor led'):
			 estab_phase='Special'
		elif row['PhaseOfEducation (name)'] in ('16 plus'):
			 estab_phase='16-plus'
		if any(trust['trust_code']==trust_code for trust in trust_list)==True:
			for trust in trust_list:
				if trust['trust_code']==trust_code:
					trust['school_count']=trust['school_count']+1
					trust['estab_type_count']['sponsored_academy_count']=trust['estab_type_count']['sponsored_academy_count']+estab_type_count['sponsored_academy_count']
					trust['estab_type_count']['converter_academy_count']=trust['estab_type_count']['converter_academy_count']+estab_type_count['converter_academy_count']
					trust['estab_type_count']['free_school_count']=trust['estab_type_count']['free_school_count']+estab_type_count['free_school_count']
					trust['estab_type_count']['utc_studio_school_count']=trust['estab_type_count']['utc_studio_school_count']+estab_type_count['utc_studio_school_count']
					break
		else:
			 trust_name_simple=re.sub('[^a-zA-Z0-9 \-\.@]', '', trust_name)
			 trust_name_simple=trust_name_simple.replace (' ', '-')
			 trust_name_simple=trust_name_simple.replace ('--', '-')
			 trust_list.append({
			 	'trust_code':trust_code,
				'trust_name':trust_name,
				'trust_name_simple':trust_name_simple,
				'trust_type':trust_type,
				'companies_house_number':companies_house_number,
				'companies_house_url':companies_house_url_stub+companies_house_number,
				'school_count':1,
				'estab_type_count':estab_type_count})


# dir=('C:/Users/pn/Documents/Work/Coding/GitHub/ainfo/data')
# os.chdir(dir)
#
# with open('trusts.json', 'w') as out_file:
#	 json.dump(trust_list, out_file)


# Sort trust_list
trust_list=sorted(trust_list, key=lambda k:k['school_count'], reverse=True)


# Create a folder for each trust with a copy of template page
path_stub='C:/Users/pn/Documents/Work/Coding/GitHub/ainfo/web/'

for trust in trust_list:
	if trust['trust_name'].lower()[0]=='a':
		path=path_stub+trust['trust_code']
		file_name=trust['trust_name_simple'].lower()+'.html'
		if not os.path.exists(path):
			os.makedirs(path)
		file_path=os.path.join(path, file_name)		# done outside the if not statement, as we want a fresh copy of the template in each case
		copy('C:/Users/pn/Documents/Work/Coding/GitHub/ainfo/trust_page_template.html', file_path)
		with open(file_path) as read_file:
			html=read_file.read()
		soup=BeautifulSoup(html, 'html.parser')
		new_h1=soup.new_tag('h1')
		new_h1.string=trust['trust_name']
		soup.body.append(new_h1)
		with open(file_path, 'w') as write_file:
			write_file.write(str(soup))


# Generate ainfo index.html
dir=('C:/Users/pn/Documents/Work/Coding/GitHub/ainfo')
os.chdir(dir)

base_url='https://philipnye.github.io/ainfo/web/'

with open('index_template.html') as read_file:
	html=read_file.read()
soup=BeautifulSoup(html, 'html.parser')
headers=['Trust name', 'Number of schools', 'Number of sponsored academies', 'Number of converter academies', 'Number of free schools', 'Number of UTCs/studio schools']
table=soup.new_tag('table')
tr=soup.new_tag('tr')
soup.div.append(table)
table.append(tr)
for header in headers:
	th=soup.new_tag('th')
	tr.append(th)
	th.append(header)
for trust in trust_list:
	trust_page_url=base_url+trust['trust_code']+'/'+trust['trust_name_simple'].lower()
	tr=soup.new_tag('tr')
	table.append(tr)
	data=[trust['trust_name'],str(trust['school_count']),str(trust['estab_type_count']['sponsored_academy_count']),str(trust['estab_type_count']['converter_academy_count']),str(trust['estab_type_count']['free_school_count']),str(trust['estab_type_count']['utc_studio_school_count'])]
	for d in data:
		td=soup.new_tag('td')
		tr.append(td)
		if d==trust['trust_name'] and d.lower()[0]=='a':
			trust_name_tag=soup.new_tag('a', href=trust_page_url)
			trust_name_tag.string=trust['trust_name']
			td.append(trust_name_tag)
		else:
			td.append(d)
soup=soup.prettify()
with open('index.html', 'w') as write_file:
	 write_file.write(str(soup))
