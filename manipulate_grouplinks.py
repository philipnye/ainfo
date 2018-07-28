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
trust_list=[]
school_list=[]
gias_url_stub='https://get-information-schools.service.gov.uk/Establishments/Establishment/Details/'
companies_house_url_stub='https://beta.companieshouse.gov.uk/company/'

github_url='https://github.com/philipnye/gias/tree/master/data'
github_raw_url='https://raw.githubusercontent.com/philipnye/gias/master/data/'

estab_phase_count={
	'primary':None,
	'secondary':None,
	'all_through':None,
	'alternative_provision':None,
	'special':None,
	'post_16':None
}

estab_type_count={
	'sponsored_academy':None,
	'converter_academy':None,
	'free_school':None,
	'utc_studio_school':None
}

html=requests.get(github_url).text
soup=BeautifulSoup(html, 'html.parser')

for a in soup.find_all('a'):
	if str(a.get('title')).endswith('csv') and str(a.get('title')).startswith('grouplinks'):
		grouplinks_file_name=str(a.get('title'))
		grouplinks_file_date=re.search('[0-9]+', grouplinks_file_name).group()
		grouplinks_file_date=datetime.datetime.strptime(grouplinks_file_date, '%Y%m%d').strftime('%d %B %Y').lstrip("0")
		grouplinks_file_url=github_raw_url+grouplinks_file_name		# expectation is that there is one and only data file
	if str(a.get('title')).endswith('csv') and str(a.get('title')).startswith('edubasealldata'):
		edubasealldata_file_name=str(a.get('title'))
		edubasealldata_file_date=re.search('[0-9]+', edubasealldata_file_name).group()
		edubasealldata_file_date=datetime.datetime.strptime(edubasealldata_file_date, '%Y%m%d').strftime('%d %B %Y').lstrip("0")
		edubasealldata_file_url=github_raw_url+edubasealldata_file_name		# expectation is that there is one and only data file

grouplinks_file=requests.get(grouplinks_file_url)
grouplinks_file=grouplinks_file.iter_lines()	  # is required in order for csv file to be read correctly, without errors caused by new-line characters
grouplinks_reader=csv.DictReader(grouplinks_file)

edubasealldata_file=requests.get(edubasealldata_file_url)
edubasealldata_file=edubasealldata_file.iter_lines()	  # is required in order for csv file to be read correctly, without errors caused by new-line characters
edubasealldata_reader=csv.DictReader(edubasealldata_file)

for row in grouplinks_reader:
	if row['Group Type'].lower() in ('multi-academy trust','single-academy trust'):
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
		estab_phase_count=dict.fromkeys(estab_phase_count, 0)
		if row['PhaseOfEducation (name)'] in ('Primary','Middle deemed primary'):
			estab_phase_count['primary']=1
		elif row['PhaseOfEducation (name)'] in ('Secondary','Middle deemed secondary'):
			estab_phase_count['secondary']=1
		elif row['PhaseOfEducation (name)'] in ('All through'):
			estab_phase_count['all_through']=1
		elif row['PhaseOfEducation (name)']==('Not applicable') and row['TypeOfEstablishment (name)'] in ('Academy alternative provision converter','Academy alternative provision sponsor led','Free schools alternative provision'):
			estab_phase_count['alternative_provision']=1
		elif row['PhaseOfEducation (name)']==('Not applicable') and row['TypeOfEstablishment (name)'] in ('Academy special converter','Academy special sponsor led','Free schools special'):
			estab_phase_count['special']=1
		elif row['PhaseOfEducation (name)'] in ('16 plus'):
			estab_phase_count['post_16']=1
		if row['TypeOfEstablishment (name)'] in ('Academy sponsor led','Academy alternative provision sponsor led','Academy special sponsor led','Academy 16 to 19 sponsor led'):
			estab_type_count['sponsored_academy']=1
		elif row['TypeOfEstablishment (name)'] in ('Academy converter','Academy alternative provision converter','Academy special converter','Academy 16-19 converter'):
			estab_type_count['converter_academy']=1
		elif row['TypeOfEstablishment (name)'] in ('Free schools','Free schools alternative provision','Free schools special','Free schools 16 to 19'):
			estab_type_count['free_school']=1
		elif row['TypeOfEstablishment (name)'] in ('University technical college','Studio schools'):
			estab_type_count['utc_studio_school']=1
		if any(trust['trust_code']==trust_code for trust in trust_list)==True:
			for trust in trust_list:
				if trust['trust_code']==trust_code:
					trust['school_count']+=1
					trust['estab_phase_count']['primary']+=estab_phase_count['primary']
					trust['estab_phase_count']['secondary']+=estab_phase_count['secondary']
					trust['estab_phase_count']['all_through']+=estab_phase_count['all_through']
					trust['estab_phase_count']['alternative_provision']+=estab_phase_count['alternative_provision']
					trust['estab_phase_count']['special']+=estab_phase_count['special']
					trust['estab_phase_count']['post_16']+=estab_phase_count['post_16']
					trust['estab_type_count']['sponsored_academy']+=estab_type_count['sponsored_academy']
					trust['estab_type_count']['converter_academy']+=estab_type_count['converter_academy']
					trust['estab_type_count']['free_school']+=estab_type_count['free_school']
					trust['estab_type_count']['utc_studio_school']+=estab_type_count['utc_studio_school']
					break
		else:
			 trust_name_simple=re.sub('[^a-zA-Z0-9 \-\.@]', '', trust_name).lower()
			 trust_name_simple=trust_name_simple.replace (' ', '-')
			 trust_name_simple=trust_name_simple.replace ('--', '-')
			 trust_page_url='web/'+trust_code+'/'+trust_name_simple+'.html'
			 trust_list.append({
			 	'trust_code':trust_code,
				'trust_name':trust_name,
				'trust_name_simple':trust_name_simple,
				'trust_page_url':trust_page_url,
				'trust_type':trust_type,
				'companies_house_number':companies_house_number,
				'companies_house_url':companies_house_url_stub+companies_house_number,
				'school_count':1,
				'estab_type_count':estab_type_count,
				'estab_phase_count':estab_phase_count,
				'pupil_numbers':0,
				'pupil_numbers_schools':0,
				'no_pupil_numbers_schools':0
			})

for row in edubasealldata_reader:
	if row['EstablishmentTypeGroup (name)'].lower() in ('academies','free schools') and row['EstablishmentStatus (name)'].lower() in ('open', 'open, but proposed to close'):
		pupils=row['NumberOfPupils']
		urn=row['URN']
		laestab=row['LA (code)']+row['EstablishmentNumber']
		la=row['LA (name)']
		region=row['GOR (name)']
		estab_name=row['EstablishmentName']
		estab_name=estab_name.replace('\xa0', ' ')		# replace characters that will prevent saving as JSON
		estab_name=estab_name.replace('\x92', '\'')
		estab_name=estab_name.replace('\xc9', 'E')
		estab_name=estab_name.replace('\xE0', 'a')
		estab_name=estab_name.replace('\x96', '-')
		type_of_estab=row['TypeOfEstablishment (name)']
		estab_status=row['EstablishmentStatus (name)']
		open_date=row['OpenDate']
		phase=row['PhaseOfEducation (name)']
		gender=row['Gender (name)']
		religious_character=row['ReligiousCharacter (name)']
		admissions_policy=row['AdmissionsPolicy (name)']
		capacity=row['SchoolCapacity']
		percentage_fsm=row['PercentageFSM']
		trust_school_flag=row['TrustSchoolFlag (name)']
		trust_name=row['Trusts (name)']
		trust_name=trust_name.replace('\xa0', ' ')		# replace characters that will prevent saving as JSON
		trust_name=trust_name.replace('\x92', '\'')
		trust_name=trust_name.replace('\xc9', 'E')
		trust_code=row['Trusts (code)']
		school_sponsor_flag=row['SchoolSponsorFlag (name)']
		school_sponsor_name=row['SchoolSponsors (name)']
		school_sponsor_name=school_sponsor_name.replace('\xa0', ' ')		# replace characters that will prevent saving as JSON
		school_sponsor_name=school_sponsor_name.replace('\x92', '\'')
		school_sponsor_name=school_sponsor_name.replace('\xc9', 'E')
		federation_flag=row['FederationFlag (name)']
		federation_name=row['Federations (name)']
		easting=row['Easting']
		northing=row['Northing']
		gias_page_url=gias_url_stub + urn
		school_list.append({
			'urn':urn,
			'laestab':laestab,
			'estab_name':estab_name,
			'pupils':pupils,
			'percentage_fsm':percentage_fsm,
			'la':la,
			'region':region,
			'phase':phase,
			'type_of_estab':type_of_estab,
			'open_date':open_date,
			'trust_name':trust_name,
			'trust_code':trust_code,
			'school_sponsor_name':school_sponsor_name
		})
		for trust in trust_list:
			if trust['trust_code']==trust_code:
				if pupils=='':
					trust['no_pupil_numbers_schools']+=1
				else:
					trust['pupil_numbers']+=int(pupils)
					trust['pupil_numbers_schools']+=1
				break

dir=('C:/Users/pn/Documents/Work/Coding/GitHub/ainfo/data')
os.chdir(dir)

with open('trusts.json', 'w') as out_file:
	 json.dump(trust_list, out_file)

with open('schools.json', 'w') as out_file:
	 json.dump(school_list, out_file)

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
		new_script=soup.new_tag('script')
		new_script.string='var trust_code='+trust['trust_code']
		soup.head.append(new_script)
		new_h1=soup.new_tag('h1')
		new_h1.string=trust['trust_name']
		soup.find(id='trust_name').append(new_h1)
		soup.find(id='gias_date').append(grouplinks_file_date)
		soup=soup.prettify()
		with open(file_path, 'w') as write_file:
			write_file.write(str(soup))

# Generate ainfo index.html
dir=('C:/Users/pn/Documents/Work/Coding/GitHub/ainfo')
os.chdir(dir)

with open('index_template.html') as read_file:
	html=read_file.read()
soup=BeautifulSoup(html, 'html.parser')
soup.find(id='gias_date').append(grouplinks_file_date)
soup=soup.prettify()
with open('index.html', 'w') as write_file:
	 write_file.write(str(soup))
