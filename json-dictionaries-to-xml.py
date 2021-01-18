import json 
import sys
import xml.etree.ElementTree as ET
import xml.dom.minidom as MD

inputfile = sys.argv[1]

data=''
with open(inputfile) as json_file: 
    data = json.load(json_file) 

for i in data['dictionaries']:
	print(i)
	root = ET.Element("DatasetDefinition")
	root.set("Action", "create")
	root.set("TableName", i['code'])
	root.set("xmlns", "http://aridhia.com/ddf")

	Title = ET.SubElement(root, "Title")
	Title.text = i['name']

	Code = ET.SubElement(root, "ID")
	Code.text = i['code']

	Url = ET.SubElement(root, "Url")
	Url.text = ''

	Description = ET.SubElement(root, "Description")
	Description.text = i['description']

	Columns = ET.SubElement(root, "Columns")

	for j in i['fields']:
	
		Column = ET.SubElement(Columns, "Column")
		Column.set("Description", j['description'])
		Column.set("Label", j['label'])
		Column.set("Name", j['name'])
		Column.set("Type", j['type'])

	outputfile = i['code'] + ".xml"

	xmlstr = MD.parseString(ET.tostring(root)).toprettyxml(indent="   ")

	with open(outputfile, "wb") as f:
	
		f.write(xmlstr.encode("utf-8"))