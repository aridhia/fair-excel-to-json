import pandas as pd, json, xlsxwriter, argparse, config

script_args=''


def parse_arguments():
    global script_args
    parser = argparse.ArgumentParser()

    parser.add_argument('-i', action='store', dest='input_file',
                                    help='Path to the input file', required=True)

    parser.add_argument('-o', action='store', dest='output_file',
                                    help='Output filename with .xlsx', required=True)

    script_args = parser.parse_args()



def read_json():
	with open(script_args.input_file) as json_file:
	    data = json.load(json_file)
	return data 

def convert_configuration(configuration_data):	
	config.log_message("Converting configuration to Excel sheet...")
	keys=[]
	values=[]

	for key in configuration_data:
		if key in ('visibility','workflow_key','code'):
			keys.append(key)
			values.append(configuration_data[key])

	data={'key':keys,'value':values}
	df=pd.DataFrame(data=data)
	config.log_message("Done!")
	return df

def convert_catalogue(catalogue_data):	
	config.log_message("Converting catalogue to Excel sheet...")
	keys=[]
	values=[]
	
	for key in catalogue_data:
		if key == 'publisher':
			keys.append('publisher_name')
			values.append(catalogue_data[key]['name'])
			if 'url' in catalogue_data[key].keys():
				keys.append('publisher_url')
				values.append(catalogue_data[key]['url'])
		elif key == 'keyword':
			keys.append('keyword')
			values.append(','.join(catalogue_data[key]))
		else:
			keys.append(key)
			values.append(catalogue_data[key])

	data={'key':keys,'value':values}
	df=pd.DataFrame(data=data)
	config.log_message("Done!")
	return df

def convert_dictionaries(dict_data):
	config.log_message("Converting dictionaries to Excel sheet...")
	codes=[]
	names=[]
	descriptions=[]

	for dictionary in dict_data:
		codes.append(dictionary['code'])
		names.append(dictionary['name'])
		descriptions.append(dictionary['description'])		

	data={'code':codes,'name':names,'description':descriptions}

	df=pd.DataFrame(data=data)
	config.log_message("Done!")

	return df

def convert_fields(dict_data):
	config.log_message("Converting fields to Excel sheet...")
	dict_names=[]
	names=[]
	labels=[]
	types=[]
	constraints=[]
	descriptions=[]

	for dictionary in dict_data:
		for field in dictionary['fields']:
			dict_names.append(dictionary['code'])
			names.append(field['name'])
			labels.append(field['label'])
			types.append(field['type'])
			constraints.append(field['constraints'])	
			descriptions.append(field['description'])			

	data={'dictionary_code':dict_names,'name': names, 'label':labels,'type': types, 'constraints':constraints, 'description':descriptions}

	df=pd.DataFrame(data=data)
	config.log_message("Done!")
	return df


def convert_lookups(dict_data):
	config.log_message("Converting lookups to Excel sheet...")

	lookup_names=[]
	field_names=[]
	descriptions=[]
	
	for dictionary in dict_data:
		for lookup in dictionary['lookups']:
			for vocab in dictionary['lookups'][lookup]['options']:
				lookup_names.append(lookup)
				field_names.append(vocab['name'])
				descriptions.append(vocab['description'])
			
	data={'lookup':lookup_names,'name':field_names,'description': descriptions}

	df=pd.DataFrame(data=data)
	config.log_message("Done!")
	return df	

def write_to_excel(dataframes):
	config.log_message("Writing Excel sheets...")

	writer = pd.ExcelWriter(script_args.output_file, engine='xlsxwriter')

	for df in dataframes:
		dataframes[df].to_excel(writer, sheet_name=df, index=False)
	
	writer.save()
	config.log_message("Conversion Complete. The Excel file can be found at '" + str(script_args.output_file)+"'")



def convert_to_excel(data):
	dataframes={}
	dataframes['configuration']=convert_configuration(data)
	dataframes['catalogue']=convert_catalogue(data['catalogue'])
	dataframes['dictionaries']=convert_dictionaries(data['dictionaries'])
	dataframes['fields']=convert_fields(data['dictionaries'])
	dataframes['lookups']=convert_lookups(data['dictionaries'])

	return dataframes	


parse_arguments()
dataframes=convert_to_excel(read_json())
write_to_excel(dataframes)