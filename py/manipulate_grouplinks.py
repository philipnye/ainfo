#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import csv
import re
import datetime
import json
import requests
import unicodedata
from num2words import num2words
from shutil import copy
from bs4 import BeautifulSoup
from bs4 import NavigableString
from unidecode import unidecode

# Create trust_list - a list of dictionaries, with one per trust. Add trusts that don't already feature in the list, and iterate the number of schools where they do
total_list=[]
trust_list=[]
sponsor_list=[]
group_list=[]
group_list_demo=[]
school_list=[]
gias_url_stub='https://get-information-schools.service.gov.uk/Establishments/Establishment/Details/'
companies_house_url_stub='https://beta.companieshouse.gov.uk/company/'

github_url='https://github.com/philipnye/gias/tree/master/data'
github_raw_url='https://raw.githubusercontent.com/philipnye/gias/master/data/'

estab_phase_count={
	'primary': None,
	'secondary': None,
	'all_through': None,
	'alternative_provision': None,
	'special': None,
	'post_16': None
}

estab_type_count={
	'sponsored_academy': None,
	'converter_academy': None,
	'free_school': None,
	'utc_studio_school': None
}

region_count={
	'east_midlands': None,
	'east_of_england': None,
	'london': None,
	'north_east': None,
	'north_west': None,
	'south_east': None,
	'south_west': None,
	'west_midlands': None,
	'yorkshire_and_the_humber': None,
}

school_count_ts={
	"201701": None,
	"201704": None,
	"201707": None,
	"201710": None,
	"201801": None,
	"201804": None,
	"201807": None,
	"201810": None,
	"201901": None,
	"201904": None,
	"201905": None		# XXX
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

def get_basic_object_info(object_code, object_name, object_type, urn):
	object_code=int(object_code)
	object_name=object_name.decode('windows-1252')
	object_name_simple=unidecode(object_name)		# replace accented characters with unaccented version
	object_name=object_name.encode('utf-8')		# decoded then encoded, so that non-utf-8 characters don't prevent saving to json files
	urn=int(urn)
	return object_code, object_name, object_name_simple, object_type, urn

def group_estab_phases(estab_phase, estab_type):
	if estab_phase in ('Primary','Middle deemed primary'):
		estab_phase='Primary'
	elif estab_phase in ('Secondary','Middle deemed secondary'):
		estab_phase='Secondary'
	elif estab_phase in ('All through'):
		estab_phase='All through'
	elif estab_phase==('Not applicable') and estab_type in ('Academy alternative provision converter','Academy alternative provision sponsor led','Free schools alternative provision'):
		estab_phase='Alternative provision'
	elif estab_phase==('Not applicable') and estab_type in ('Academy special converter','Academy special sponsor led','Free schools special'):
		estab_phase='Special'
	elif estab_phase in ('16 plus'):
		estab_phase='Post-16'
	return estab_phase

def count_grouped_estab_phases(estab_phase):
	estab_phase_string=estab_phase.lower()
	estab_phase_string=replace_spaces_slashes_hypens(estab_phase_string)
	estab_phase_count[estab_phase_string]=1
	return estab_phase_count

def group_estab_types(estab_type):
	if estab_type in ('Academy sponsor led','Academy alternative provision sponsor led','Academy special sponsor led','Academy 16 to 19 sponsor led'):
		estab_type='Sponsored academy'
	elif estab_type in ('Academy converter','Academy alternative provision converter','Academy special converter','Academy 16-19 converter'):
		estab_type='Converter academy'
	elif estab_type in ('Free schools','Free schools alternative provision','Free schools special','Free schools 16 to 19'):
		estab_type='Free school'
	elif estab_type in ('University technical college','Studio schools'):
		estab_type='UTC/studio school'
	return estab_type

def count_grouped_estab_types(estab_type):
	estab_type_string=estab_type.lower()
	estab_type_string=replace_spaces_slashes_hypens(estab_type_string)
	estab_type_count[estab_type_string]=1
	return estab_type_count

def count_regions(region):
	region_string=region.lower()
	region_string=replace_spaces_slashes_hypens(region_string)
	region_count[region_string]=1
	return region_count

def produce_group_page_url(object_name_simple,object_code):
	group_name_url=re.sub('[^a-zA-Z0-9\']', '-', object_name_simple.lower())
	group_name_url=re.sub('\'', '', group_name_url)
	group_name_url=re.sub('-+', '-', group_name_url)
	group_name_url=re.sub('-$', '', group_name_url)
	group_page_url='web/'+str(object_code)+'/'+group_name_url+'.html'
	return group_name_url, group_page_url

def replace_spaces_slashes_hypens(word):
	word=re.sub(' ', '_', word)
	word=re.sub('/', '_', word)
	word=re.sub('-','_', word)
	return word

def reformat_region_names(word):
	word=re.sub('_',' ',word)
	word=re.sub('england','England',word)
	word=re.sub('london','London',word)
	word=re.sub('midlands','Midlands',word)
	word=re.sub('yorkshire','Yorkshire',word)
	word=re.sub('humber','Humber',word)
	return word

def write_group_description(group):
	if group['school_count']<=5:
		group_desc_size='small'
	elif group['school_count']<=10:
		group_desc_size='medium-sized'
	else:
		group_desc_size='large'
	region_tally=0
	region_list=[]
	for region in group['region_count']:
		if group['region_count'][region]>0:
			region_tally+=1
			region_list.append(region)
	if region_tally==1 and region_list[0].lower()=='london':
		group_desc_regions=reformat_region_names(region_list[0]) + ' only'
	elif region_tally==1 and region_list[0].lower()!='london':
		group_desc_regions='the ' + reformat_region_names(region_list[0]) + ' only'
	else:
		group_desc_regions=num2words(region_tally).decode('windows-1252').encode('utf-8') + ' regions'
	if group['school_count']<10:
		group_desc_school_count=num2words(group['school_count']).decode('windows-1252').encode('utf-8')
	else:
		group_desc_school_count=str(group['school_count'])
	if group['school_count']==1:
		group_desc_estab='academy'
	else:
		group_desc_estab='academies'
	phase_tally=0
	phase_list=[]
	for phase in group['estab_phase_count']:
		if group['estab_phase_count'][phase]>0:
			phase_tally+=1
			phase_list.append(phase)
	if phase_tally==1:
		group_desc_phase_1=phase_list[0] + ' '
		group_desc_phase_2=''
	elif phase_tally==2:
		group_desc_phase_1=''
		group_desc_phase_2=' across two different phases'
	else:
		group_desc_phase_1=''
		group_desc_phase_2=' across a mix of phases'
	group['description']=group['group_name'] + ' is a ' + group_desc_size + ' group which operates in ' + group_desc_regions + '. The group runs ' + group_desc_school_count + ' ' + group_desc_phase_1 + group_desc_estab + group_desc_phase_2 + '.'
	return

# Build trust_list and sponsor_list
for row in grouplinks_reader:
	if row['Group Type'].lower() in ('multi-academy trust','single-academy trust'):
		trust_code, trust_name, trust_name_simple, group_type, urn=get_basic_object_info(row['Linked UID'], row['Group Name'], row['Group Type'], row['URN'])
		companies_house_number=row['Companies House Number']
		school_count_ts=dict.fromkeys(school_count_ts, 0)
		estab_phase=group_estab_phases(row['PhaseOfEducation (name)'], row['TypeOfEstablishment (name)'])
		estab_phase_count=dict.fromkeys(estab_phase_count, 0)
		count_grouped_estab_phases(estab_phase)
		estab_type=group_estab_types(row['TypeOfEstablishment (name)'])
		estab_type_count=dict.fromkeys(estab_type_count, 0)
		count_grouped_estab_types(estab_type)
		region_count=dict.fromkeys(region_count, 0)
		if any(trust['trust_code']==trust_code for trust in trust_list)==True:
			for trust in trust_list:
				if trust['trust_code']==trust_code:
					trust['school_count']+=1
					trust['school_count_ts']={ k: trust['school_count_ts'].get(k, 0) + 1 for k in set(trust['school_count_ts']) }
					trust['estab_phase_count']={ k: trust['estab_phase_count'].get(k, 0) + estab_phase_count.get(k, 0) for k in set(trust['estab_phase_count']) & set(estab_phase_count) }
					trust['estab_type_count']={ k: trust['estab_type_count'].get(k, 0) + estab_type_count.get(k, 0) for k in set(trust['estab_type_count']) & set(estab_type_count) }
					trust['region_count']={ k: trust['region_count'].get(k, 0) + region_count.get(k, 0) for k in set(trust['region_count']) & set(region_count) }
					trust['urns'].append(urn)
					break
		else:
			trust_list.append({
				'trust_code': trust_code,
				'trust_name': trust_name,
				'trust_name_simple': trust_name_simple,
				'group_type': group_type,
				'companies_house_number': companies_house_number,
				'companies_house_url': companies_house_url_stub+companies_house_number,
				'school_count': 1,
				'school_count_ts': dict.fromkeys(school_count_ts, 1),
				'estab_type_count': estab_type_count.copy(),		# done to ensure a separate dictionary is created for each trust
				'estab_phase_count': estab_phase_count.copy(),		#	"	"
				'region_count': region_count.copy(),
				'pupil_numbers': 0,
				'pupil_numbers_schools': 0,
				'no_pupil_numbers_schools': 0,
				'urns': [urn]
			})
	elif row['Group Type'].lower()=='school sponsor':
		sponsor_code, sponsor_name, sponsor_name_simple, group_type, urn=get_basic_object_info(row['Linked UID'], row['Group Name'], row['Group Type'], row['URN'])
		if any(sponsor['sponsor_code']==sponsor_code for sponsor in sponsor_list)==True:
			for sponsor in sponsor_list:
				if sponsor['sponsor_code']==sponsor_code:
					sponsor['urns'].append(urn)
					break
		else:
			sponsor_list.append({
				'sponsor_code':sponsor_code,
				'sponsor_name':sponsor_name,
				'sponsor_name_simple':sponsor_name_simple,
				'group_type':group_type,
				'urns':[urn],
				'trusts': None
			})

for trust in trust_list:
	for urn in trust['urns']:
		for sponsor in sponsor_list:
			if any(spon_urn==urn for spon_urn in sponsor['urns'])==True:
				if sponsor['trusts']==None:
					sponsor['trusts']=[{
						'trust_code':trust['trust_code'],
						'trust_name':trust['trust_name'],
						'companies_house_number':trust['companies_house_number'],
						'companies_house_url':trust['companies_house_url']
					}]
				elif any(spon_trust['trust_code']==trust['trust_code'] for spon_trust in sponsor['trusts'])==False:
					sponsor['trusts'].append({
						'trust_code':trust['trust_code'],
						'trust_name':trust['trust_name'],
						'companies_house_number':trust['companies_house_number'],
						'companies_house_url':trust['companies_house_url']
					})
					break
				break

# Create school-level data
for row in edubasealldata_reader:
	if row['EstablishmentTypeGroup (name)'].lower() in ('academies','free schools') and row['EstablishmentStatus (name)'].lower() in ('open', 'open, but proposed to close'):
		pupils=row['NumberOfPupils']
		urn=int(row['URN'])
		laestab=int(row['LA (code)']+row['EstablishmentNumber'])
		la=row['LA (name)']
		region=row['GOR (name)']
		estab_name=row['EstablishmentName'].decode('windows-1252').encode('utf-8')
		estab_phase=group_estab_phases(row['PhaseOfEducation (name)'],row['TypeOfEstablishment (name)'])
		estab_type=group_estab_types(row['TypeOfEstablishment (name)'])
		estab_status=row['EstablishmentStatus (name)']
		open_date=row['OpenDate']
		gender=row['Gender (name)']
		religious_character=row['ReligiousCharacter (name)']
		admissions_policy=row['AdmissionsPolicy (name)']
		capacity=row['SchoolCapacity']
		percentage_fsm=row['PercentageFSM']
		trust_name=row['Trusts (name)'].decode('windows-1252').encode('utf-8')
		if row['Trusts (code)']!='':		# XXX handle the small number of academies in GIAS data with no trust and TrustSchoolFlag (name) status of 'Not supported by a trust'
			trust_code=int(row['Trusts (code)'])
		else:
			trust_code=None
		sponsor_name=row['SchoolSponsors (name)'].decode('windows-1252').encode('utf-8')
		if row['Easting']!='' and row['Northing']!='':
			easting=int(row['Easting'])
			northing=int(row['Northing'])
		else:
			easting=northing=None
		gias_page_url=gias_url_stub+str(urn)
		school_list.append({
			'urn':urn,
			'laestab':laestab,
			'estab_name':estab_name,
			'pupils':pupils,
			'percentage_fsm':percentage_fsm,
			'la':la,
			'region':region,
			'estab_phase':estab_phase,
			'estab_type':estab_type,
			'open_date':open_date,
			'trust_name':trust_name,
			'trust_code':trust_code,
			'sponsor_name':sponsor_name
		})
		for trust in trust_list:
			if trust['trust_code']==trust_code:
				if pupils=='':
					trust['no_pupil_numbers_schools']+=1
				else:
					trust['pupil_numbers']+=int(pupils)
					trust['pupil_numbers_schools']+=1
				region_count=dict.fromkeys(region_count, 0)
				count_regions(region)
				trust['region_count']={ k: trust['region_count'].get(k, 0) + region_count.get(k, 0) for k in set(trust['region_count']) & set(region_count) }		# addition of two dictionaries with matching keys
				break

# Build group_list
school_count_ts=dict.fromkeys(school_count_ts, 0)
estab_phase_count=dict.fromkeys(estab_phase_count, 0)
estab_type_count=dict.fromkeys(estab_type_count, 0)
region_count=dict.fromkeys(region_count, 0)

for sponsor in sponsor_list:
	if len(sponsor['trusts'])>1:
		group_list.append(sponsor.copy())		# done to ensure a separate dictionary is created for each group
		group_name_url, group_page_url=produce_group_page_url(sponsor['sponsor_name_simple'],sponsor['sponsor_code'])
		group_list[-1]['group_name_url']=group_name_url
		group_list[-1]['group_page_url']=group_page_url
		group_list[-1]['school_count']=0
		group_list[-1]['school_count_ts']=school_count_ts.copy()		#	"	"
		group_list[-1]['estab_phase_count']=estab_phase_count.copy()		#	"	"
		group_list[-1]['estab_type_count']=estab_type_count.copy()		#	"	"
		group_list[-1]['region_count']=region_count.copy()		#	"	"
		group_list[-1]['pupil_numbers']=0
		group_list[-1]['pupil_numbers_schools']=0
		group_list[-1]['no_pupil_numbers_schools']=0

for trust in trust_list:		# group values are built in this way from trust-level figures as grouplinks can't be used directly to get these values for sponsors, as in most cases non-sponsored academies aren't listed against a sponsor
	group_present=False
	for group in group_list:
		if group['group_type'].lower()=="school sponsor":		# done as we start adding trusts (as opposed to sponsors) to group_list, which don't have trust['trusts']
			if any(group_trust['trust_code']==trust['trust_code'] for group_trust in group['trusts'])==True:
				group_present=True
				group['school_count']+=trust['school_count']
				group['school_count_ts']={ k: group['school_count_ts'].get(k, 0) + trust['school_count'] for k in set(group['school_count_ts']) }
				group['estab_phase_count']={ k: group['estab_phase_count'].get(k, 0) + trust['estab_phase_count'].get(k, 0) for k in set(group['estab_phase_count']) & set(trust['estab_phase_count']) }
				group['estab_type_count']={ k: group['estab_type_count'].get(k, 0) + trust['estab_type_count'].get(k, 0) for k in set(group['estab_type_count']) & set(trust['estab_type_count']) }
				group['region_count']={ k: group['region_count'].get(k, 0) + trust['region_count'].get(k, 0) for k in set(group['region_count']) & set(trust['region_count']) }
				group['pupil_numbers']+=trust['pupil_numbers']
				group['pupil_numbers_schools']+=trust['pupil_numbers_schools']
				group['no_pupil_numbers_schools']+=trust['no_pupil_numbers_schools']
				break
	if group_present==False:
		group_list.append(trust.copy())		# done to ensure a separate dictionary is created for each group
		group_name_url, group_page_url=produce_group_page_url(trust['trust_name_simple'],trust['trust_code'])
		group_list[-1]['group_name_url']=group_name_url
		group_list[-1]['group_page_url']=group_page_url
		group_list[-1]['trusts']=None

for group in group_list:
	for key in group.keys():
		if key.split('_')[0]=='sponsor' or key.split('_')[0]=='trust':
			if key.split('_')[0]=='sponsor':
				renamed_key=re.sub('sponsor', 'group', key)
			elif key.split('_')[0]=='trust':
				renamed_key=re.sub('trust', 'group', key)
			group[renamed_key]=group[key]
			group.pop(key)
	write_group_description(group)

group_list_demo=group_list[:]		# copy operation for lists
group_list_demo[:]=[d for d in group_list_demo if d.get('group_name').lower()[0]=='a']		# removes every group that doesn't start with 'a'

# Set the group_code against which schools should be reported in school_list
for school in school_list:
	for group in group_list:
		if group['group_type'].lower()=='school sponsor':
			if any(trust['trust_code']==school['trust_code'] for trust in group['trusts'])==True:
				school['group_code']=group['group_code']
				break
		elif group['group_type'].lower()!='school sponsor':
			if group['group_code']==school['trust_code']:
				school['group_code']=school['trust_code']
				break

# Create overall totals
school_count=group_count=0
estab_phase_count = dict.fromkeys(estab_phase_count, 0)
estab_type_count = dict.fromkeys(estab_type_count, 0)
region_count = dict.fromkeys(estab_type_count, 0)

for group in group_list:		# XXX: in creating totals using grouplinks file, misses out a small number of academies - those in GIAS data with no trust and TrustSchoolFlag (name) status of 'Not supported by a trust'
	school_count+=group['school_count']
	group_count+=1
	estab_phase_count={ k: estab_phase_count.get(k, 0) + group['estab_phase_count'].get(k, 0) for k in set(estab_phase_count) & set(group['estab_phase_count']) }
	estab_type_count={ k: estab_type_count.get(k, 0) + group['estab_type_count'].get(k, 0) for k in set(estab_type_count) & set(group['estab_type_count']) }
	region_count={ k: region_count.get(k, 0) + group['region_count'].get(k, 0) for k in set(region_count) & set(group['region_count']) }

total_list.append({
	'school_count':school_count,
	'group_count': group_count,
	'estab_type_count':estab_type_count,
	'estab_phase_count':estab_phase_count,
	'region_count':estab_phase_count,
})

# Save data to json files
os.chdir(os.path.dirname( __file__ ))
os.chdir('..')
os.chdir('data')

with open('totals.json', 'w') as out_file:
	json.dump(total_list, out_file, indent=4, separators=(',', ': '))

with open('trusts.json', 'w') as out_file:
	json.dump(trust_list, out_file, indent=4, separators=(',', ': '))

with open('sponsors.json', 'w') as out_file:
	json.dump(sponsor_list, out_file, indent=4, separators=(',', ': '))

with open('groups.json', 'w') as out_file:
	json.dump(group_list, out_file, indent=4, separators=(',', ': '))

with open('groups_demo.json', 'w') as out_file:
	json.dump(group_list_demo, out_file, indent=4, separators=(',', ': '))

with open('schools.json', 'w') as out_file:
	json.dump(school_list, out_file, indent=4, separators=(',', ': '))

# Create group pages
os.chdir(os.path.dirname( __file__ ))
os.chdir('..')
group_page_path_stub=os.getcwd()+'\\web\\'
os.chdir(os.path.dirname( __file__ ))
os.chdir('..')
template_path=os.getcwd()+'\\templates\\group_page_template.html'

with open(template_path) as read_file:
	html=read_file.read()

for group in group_list:
	if group['group_name'].lower()[0]=='a':
		group_page_path=group_page_path_stub+str(group['group_code'])
		file_name=group['group_name_url']+'.html'
		if os.path.exists(group_page_path):
			for existing_file in os.listdir(group_page_path):
				existing_file_path=os.path.join(group_page_path, existing_file)
				os.remove(existing_file_path)
		else:
			os.makedirs(group_page_path)
		file_path=os.path.join(group_page_path, file_name)		# done outside the if not statement, as we want a fresh copy of the template in each case
		copy(template_path, file_path)
		soup=BeautifulSoup(html, 'html.parser')
		with open(file_path, 'w') as write_file:
			write_file.write(str(soup))

# Update ainfo index.html
os.chdir(os.path.dirname( __file__ ))
os.chdir('..')
