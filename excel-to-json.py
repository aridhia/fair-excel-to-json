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
def read_sheet(sheet_name):
	global script_args
	return pd.read_excel(io=script_args.input_file,sheet_name=sheet_name)


# Get catalogue information
def create_catalogue_section():
	config.log_message("Converting the catalogue to JSON...")
	pd = read_sheet('catalogue')
	pd=pd.dropna()

	result = pd.to_dict(orient="records")
	supported_values=['id','title','description', 'creator','contactPoint','publisher_name','publisher_url','license','versionInfo','keyword','identifier','rights']
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
	pd = read_sheet('dictionaries')
	dictionaries = pd.to_dict(orient="records")

	dicts_arr=[]
	for row in dictionaries:
		config.log_message("Converting dictionary '" + row['name'] + "' to JSON...")

		fields_dict={}
		fields_dict['id']=row['name']
		fields_dict['description']=row['description']
		fields,lookups=create_fields_json(row['name'])
		fields_dict['fields']=fields
		fields_dict['lookups']=lookups
		dicts_arr.append(fields_dict)

		config.log_message("Done!")
	return dicts_arr	


# Get fields for a dictionary
def create_fields_json(dictionary_name):
	config.log_message("-- Converting fields to JSON...")
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
	config.log_message("-- Converting lookup: '" + lookup_name + "' to JSON...")
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
	
# Create top level JSON: datasets, catalogues, dictionaries
def create_json_structure():
	config.log_message("Converting Excel to FAIR JSON...")
	json_dict={}
	json_dict['catalogue']=create_catalogue_section()
	json_dict['dictionaries']=create_dictionary_section()

	json_content=json.dumps(json_dict, indent=4)

	f = open(script_args.output_file, "a")
	f.write(json_content)
	f.close()	
	config.log_message("Conversion Complete. The FAIR JSON can be in the file '" + str(script_args.output_file)+"'")

parse_arguments()
create_json_structure()


