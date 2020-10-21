import pandas as pd
import json
import numpy as np
import argparse

script_args=''


def parse_arguments():
    global script_args
    parser = argparse.ArgumentParser()

    parser.add_argument('-i', action='store', dest='input_file',
                                    help='Path to the input file', required=True)

    parser.add_argument('-o', action='store', dest='output_file',
                                    help='Output filename with .json', required=True)

    script_args = parser.parse_args()

# Read Excel Sheet
def read_sheet(sheet_name):
	global script_args
	print(script_args)
	return pd.read_excel(io=script_args.input_file,sheet_name=sheet_name)

# Create top level JSON: datasets, catalogues, dictionaries
def create_json_structure():
	

	datasets_arr=[]
	json_dict={}
	json_dict['catalogue']=create_catalogue_section()
	json_dict['dictionaries']=create_dictionary_section()
	datasets_arr.append(json_dict)

	datasets_dict={}
	datasets_dict['datasets']=datasets_arr

	json_content=json.dumps(datasets_dict, indent=4)
	print(json_content)

	f = open(script_args.output_file, "a")
	f.write(json_content)
	f.close()

# Get catalogue information
def create_catalogue_section():
	pd = read_sheet('catalogue')
	pd=pd.dropna()

	result = pd.to_dict(orient="records")

	catalogue_dict={}
	publisher={}
	for row in result:
		print(row)
		if row['value']!='to_be_excluded':

			# Those that need more work to get into required structure
			if row['key']=='publisher_name':
				publisher['name']=row['value']
			elif row['key']=='publisher_url':
				publisher['url']=row['value']	
			elif row['key']=='keyword':
				catalogue_dict['keyword']=row['value'].split(",")
			else:
				catalogue_dict[row['key']]=row['value']

	catalogue_dict["publisher"]=publisher	

	return catalogue_dict	

# Get dictionary information
def create_dictionary_section():
	pd = read_sheet('dictionaries')
	dictionaries = pd.to_dict(orient="records")

	dicts_arr=[]
	for row in dictionaries:
		fields_dict={}
		fields_dict['id']=row['name']
		fields,lookups=create_fields_json(row['name'])
		fields_dict['fields']=fields
		fields_dict['lookups']=lookups
		dicts_arr.append(fields_dict)

	return dicts_arr	


# Get fields for a dictionary
def create_fields_json(dictionary_name):
	pd = read_sheet('fields')
	pd=pd.replace(np.nan,"null")
	result = pd.to_dict(orient="records")

	fields_arr=[]
	constraints_arr=[]
	for row in result:
		if row['dictionary_name']==dictionary_name:
			fields_dict={}
			fields_dict['name']=row['name']
			fields_dict['label']=row['label']
			fields_dict['type']=row['type']
			fields_dict['constraints']=row['constraints']
			if row['constraints']!='null':
				constraints_arr.append(row['constraints'])
			fields_dict['description']=row['description']
			fields_arr.append(fields_dict)

	lookups_dict={}
	for lookup in constraints_arr:
		lookups_dict[lookup]=create_lookups_json(lookup)
	
	return fields_arr, lookups_dict


# Get lookups for a dictionary
def create_lookups_json(lookup_name):
	pd = read_sheet('lookups')
	result = pd.to_dict(orient="records")

	lookups_arr=[]
	for row in result:
		if row['lookup']==lookup_name:
			lookups_dict={}
			lookups_dict['name']=row['name']
			lookups_dict['description']=row['description']
			lookups_arr.append(lookups_dict)
	
	return lookups_arr
	

parse_arguments()
create_json_structure()


