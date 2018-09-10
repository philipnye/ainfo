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
from unidecode import unidecode

# Create trust_list - a list of dictionaries, with one per trust. Add trusts that don't already feature in the list, and iterate the number of schools where they do
total_list=[]
trust_list=[]
school_list=[]
sponsor_list=[]
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

# Create trust-level data
for row in grouplinks_reader:
	if row['Group Type'].lower() in ('multi-academy trust','single-academy trust'):
		trust_code=int(row['Linked UID'])
		trust_name=row['Group Name'].decode('windows-1252').encode('utf-8')		# decode, so that non-utf-8 characters don't prevent saving to json files
		trust_name_simple=unidecode(row['Group Name'].decode('windows-1252'))		# replace accented characters with unaccented version
		trust_name_url=re.sub('[^a-zA-Z0-9\']', '-', trust_name_simple.lower())
		trust_name_url=re.sub('\'', '', trust_name_url)
		trust_name_url=re.sub('-+', '-', trust_name_url)
		trust_name_url=re.sub('-$', '', trust_name_url)
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
			trust_page_url='web/'+str(trust_code)+'/'+trust_name_url+'.html'
			trust_list.append({
				'trust_code':trust_code,
				'trust_name':trust_name,
				'trust_name_simple':trust_name_simple,
				'trust_name_url':trust_name_url,
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

school_count=trust_count=sat_count=mat_count=0
estab_phase_count = dict.fromkeys(estab_phase_count, 0)
estab_type_count = dict.fromkeys(estab_type_count, 0)

# Create overall totals
for trust in trust_list:		# XXX: in creating totals using grouplinks file, misses out a small number of academies - those in GIAS data with no trust and TrustSchoolFlag (name) status of 'Not supported by a trust'
	school_count+=trust['school_count']
	trust_count+=1
	if trust['trust_type']=='Single-academy trust':
		sat_count+=1
	elif trust['trust_type']=='Multi-academy trust':
		mat_count+=1
	estab_phase_count['primary']+=trust['estab_phase_count']['primary']
	estab_phase_count['secondary']+=trust['estab_phase_count']['secondary']
	estab_phase_count['all_through']+=trust['estab_phase_count']['all_through']
	estab_phase_count['alternative_provision']+=trust['estab_phase_count']['alternative_provision']
	estab_phase_count['special']+=trust['estab_phase_count']['special']
	estab_phase_count['post_16']+=trust['estab_phase_count']['post_16']
	estab_type_count['sponsored_academy']+=trust['estab_type_count']['sponsored_academy']
	estab_type_count['converter_academy']+=trust['estab_type_count']['converter_academy']
	estab_type_count['free_school']+=trust['estab_type_count']['free_school']
	estab_type_count['utc_studio_school']+=trust['estab_type_count']['utc_studio_school']

total_list.append({
	'school_count':school_count,
	'trust_count': trust_count,
	'sat_count': sat_count,
	'mat_count': mat_count,
	'estab_type_count':estab_type_count,
	'estab_phase_count':estab_phase_count
})

# Create school-level data
for row in edubasealldata_reader:
	if row['EstablishmentTypeGroup (name)'].lower() in ('academies','free schools') and row['EstablishmentStatus (name)'].lower() in ('open', 'open, but proposed to close'):
		pupils=row['NumberOfPupils']
		urn=row['URN']
		laestab=row['LA (code)']+row['EstablishmentNumber']
		la=row['LA (name)']
		region=row['GOR (name)']
		estab_name=row['EstablishmentName'].decode('windows-1252').encode('utf-8')
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
		trust_name=row['Trusts (name)'].decode('windows-1252').encode('utf-8')
		if row['Trusts (code)']!='':		# XXX handle the small number of academies in GIAS data with no trust and TrustSchoolFlag (name) status of 'Not supported by a trust'
			trust_code=int(row['Trusts (code)'])
		else:
			trust_code=None
		school_sponsor_flag=row['SchoolSponsorFlag (name)']
		school_sponsor_name=row['SchoolSponsors (name)'].decode('windows-1252').encode('utf-8')
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
		if any(sponsor['school_sponsor_name']==school_sponsor_name for sponsor in sponsor_list)==True:
			for sponsor in sponsor_list:
				if sponsor['school_sponsor_name']==school_sponsor_name:
					if any(trust['trust_code']==trust_code for trust in sponsor['trusts'])==False:
						sponsor['trusts'].append({
							'trust_name':trust_name,
							'trust_code':trust_code
						})
					break
		else:
			sponsor_list.append({
				'school_sponsor_name':school_sponsor_name,
				'trusts':[{
					'trust_name':trust_name,
					'trust_code':trust_code
				}]
			})
		for trust in trust_list:
			if trust['trust_code']==trust_code:
				if pupils=='':
					trust['no_pupil_numbers_schools']+=1
				else:
					trust['pupil_numbers']+=int(pupils)
					trust['pupil_numbers_schools']+=1
				break

sponsor_list=[sponsor for sponsor in sponsor_list if len(sponsor['trusts'])>1]

for trust in trust_list:
	for sponsor in sponsor_list:
		if any(sponsor_trust['trust_code']==trust['trust_code'] for sponsor_trust in sponsor['trusts'])==True:
			trust['trust_name_loose']=sponsor['school_sponsor_name']
			break

# Save data to json files
os.chdir(os.path.dirname( __file__ ))
os.chdir('..')
os.chdir('data')

with open('totals.json', 'w') as out_file:
	json.dump(total_list, out_file, indent=4, separators=(',', ': '))

with open('trusts.json', 'w') as out_file:
	json.dump(trust_list, out_file, indent=4, separators=(',', ': '))

with open('schools.json', 'w') as out_file:
	json.dump(school_list, out_file, indent=4, separators=(',', ': '))

# Create trust pages
os.chdir(os.path.dirname( __file__ ))
os.chdir('..')
trust_page_path_stub=os.getcwd()+'\\web\\'
os.chdir(os.path.dirname( __file__ ))
os.chdir('..')
template_path=os.getcwd()+'\\templates\\trust_page_template.html'

with open(template_path) as read_file:
	html=read_file.read()

for trust in trust_list:
	if trust['trust_name'].lower()[0]=='a':
		trust_page_path=trust_page_path_stub+str(trust['trust_code'])
		file_name=trust['trust_name_url']+'.html'
		if os.path.exists(trust_page_path):
			for existing_file in os.listdir(trust_page_path):
				existing_file_path=os.path.join(trust_page_path, existing_file)
				try:
					os.unlink(existing_file_path)
				except Exception as e:
					print(e)
		else:
			os.makedirs(trust_page_path)
		file_path=os.path.join(trust_page_path, file_name)		# done outside the if not statement, as we want a fresh copy of the template in each case
		copy(template_path, file_path)
		soup=BeautifulSoup(html, 'html.parser')
		new_script=soup.new_tag('script')
		new_script.string='var trust_code='+str(trust['trust_code'])
		soup.head.append(new_script)
		new_h1=soup.new_tag('h1')
		new_h1.string=trust['trust_name_simple']
		soup.find(id='trust_name').append(new_h1)
		soup.find(id='gias_date').append(grouplinks_file_date)
		soup=soup.prettify()
		with open(file_path, 'w') as write_file:
			write_file.write(str(soup))

# Generate ainfo index.html
os.chdir(os.path.dirname( __file__ ))
os.chdir('..')

with open('index.html') as read_file:
	html=read_file.read()
soup=BeautifulSoup(html, 'html.parser')
soup.find(id='gias_date').string='GIAS date: '+grouplinks_file_date
soup=soup.prettify()
with open('index.html', 'w') as write_file:
	 write_file.write(str(soup))
