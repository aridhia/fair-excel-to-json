# Introduction 
In order to create a dataset in FAIR via the API, a JSON representation of the dataset needs to be created. In order to easily facilate this JSON creation, this repository contains:
- a FAIR metadata Excel template that can be completed with a dataset's metadata
- an Excel to FAIR JSON converter that can be used to create the dataset via the API.
- If required, a JSON to Excel converter.
- If required, a JSON to XML converter for data dictionaries.

# Pre-requisites
To run the converter script you need to have the following installed:

- [Python 3](https://www.python.org/)

The script uses the following Python3 libraries:
- pandas
- numpy
- xlsxwriter
- argparse

# Converting Excel to FAIR JSON
1. Complete the 'FAIR_Metadata_Template.xlsx' Excel spreadsheet with metadata for your dataset.
2. Run the 'excel-to-json.py' script with the following arguments:
```
-i <path_to_excel>
-i <output_filename>.json
```
For example:
```sh
python3 excel-to-json.py -i FAIR_Metadata_Template.xlsx -o dataset.json
```
# Converting FAIR JSON to Excel
If required, existing FAIR JSON can be converted to Excel, e.g. for easy or shared editing
1. Download a copy of the FAIR JSON, e.g. downloaded from FAIR or extract from the API.
2. Run the 'json-to-excel.py' script with the following arguments:
```
-i <path_to_json>
-o <output_filename>.xslx
```
For example:
```sh
python3 json-to-excel.py -i dataset.json -o excel_dataset.xlsx
```

# Converting FAIR JSON to XML
If required, data dictionaries can be converted from the resulting JSON to XML.
1. Download a copy of the FAIR JSON, e.g. downloaded from FAIR or extract from the API.
2. Run the 'json-dictionaries-to-xml.py' script. For example:
```sh
python3 json-dictionaries-to-xml.py dataset.json
```
This will provide an XML file for each data dictionary.

# Feedback
Contact Gary McGilvary (gary.mcgilvary@aridhia.com) to provide feedback




