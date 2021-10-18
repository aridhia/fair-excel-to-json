import pandas as pd
import json
import numpy as np
import argparse
import config

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
def read_sheet(sheet_name,converters):
	global script_args
	return pd.read_excel(io=script_args.input_file,sheet_name=sheet_name,converters=converters)

# Get configuration information

def create_configuration_section():
	config.log_message("Converting the configuration to JSON...")
	pd = read_sheet('configuration',{'key':str,'value':str})
	pd=pd.dropna()

	result = pd.to_dict(orient="records")
	supported_values=['visibility','workflow_key','code']
	configuration_dict={}
	for row in result:
		if row['key'] in supported_values:
			configuration_dict[row['key']]=row['value']

	config.log_message("Done!")

	return configuration_dict

# Get catalogue information
def create_catalogue_section():
	config.log_message("Converting the catalogue to JSON...")
	pd = read_sheet('catalogue',{'key':str,'value':str})
	pd=pd.dropna()

	result = pd.to_dict(orient="records")
	supported_values=['title','description','creator','contactPoint','license','versionInfo','keyword','identifier','rights','publisher_name','publisher_url']
	catalogue_dict={}
	publisher={}
	for row in result:
		if row['key'] in supported_values:
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
	config.log_message("Done!")

	return catalogue_dict	

# Get dictionary information
def create_dictionary_section():
	pd = read_sheet('dictionaries',{'code':str,'name':str,'description':str})
	dictionaries = pd.to_dict(orient="records")

	dicts_arr=[]
	for row in dictionaries:
		config.log_message("Converting dictionary '" + row['name'] + "' to JSON...")

		fields_dict={}
		fields_dict['code']=row['code']
		fields_dict['name']=row['name']
		fields_dict['description']=row['description']
		fields,lookups=create_fields_json(row['code'])
		fields_dict['fields']=fields
		fields_dict['lookups']=lookups
		dicts_arr.append(fields_dict)

		config.log_message("Done!")
	return dicts_arr	


# Get fields for a dictionary
def create_fields_json(dictionary_code):
	config.log_message("-- Converting fields to JSON...")
	pd = read_sheet('fields',{'dictionary_code':str,'name':str,'label':str,'type':str,'constraints':str,'description':str})
	pd=pd.replace(np.nan,"null")
	result = pd.to_dict(orient="records")

	fields_arr=[]
	constraints_dict={}
	for row in result:
		if row['dictionary_code']==dictionary_code:
			fields_dict={}
			fields_dict['name']=row['name']
			fields_dict['label']=row['label']
			fields_dict['type']=row['type']
			fields_dict['constraints']=row['constraints']
			if row['constraints']!='null':
				constraints_dict[row['constraints']]=row['type']
			fields_dict['description']=row['description']
			fields_arr.append(fields_dict)

	lookups_dict={}
	for constraint, type in constraints_dict.items():
		lookups_dict[constraint]=create_lookups_json(constraint, type)
	return fields_arr, lookups_dict


# Get lookups for a dictionary
def create_lookups_json(lookup_name, lookup_type):
	config.log_message("-- Converting lookup: '" + lookup_name + "' to JSON...")
	pd = read_sheet('lookups',{'lookup':str,'name':str,'description':str})
	result = pd.to_dict(orient="records")

	lookups_dict={}
	options_arr=[]
	lookups_dict['type']=lookup_type
	lookups_dict['options']=options_arr
	for row in result:
		if row['lookup']==lookup_name:
			options_dict={}
			options_dict['name']=row['name']
			options_dict['description']=str(row['description'])
			options_arr.append(options_dict)
	return lookups_dict
	
# Create top level JSON: datasets, catalogues, dictionaries
def create_json_structure():
	config.log_message("Converting Excel to FAIR JSON...")
	json_dict=create_configuration_section()
	json_dict['catalogue']=create_catalogue_section()
	json_dict['dictionaries']=create_dictionary_section()

	json_content=json.dumps(json_dict, indent=4)

	f = open(script_args.output_file, "a")
	f.write(json_content)
	f.close()	
	config.log_message("Conversion Complete. The FAIR JSON can be found in the file '" + str(script_args.output_file)+"'")

parse_arguments()
create_json_structure()


