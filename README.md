# Introduction 
In order to create a dataset in FAIR via the API, a JSON representation of the dataset needs to be created. In order to easily facilate this JSON creation, this repository contains:
- a FAIR metadata Excel template that can be completed with a dataset's metadata
- an Excel to FAIR JSON convertor that can be used to create the dataset via the API.

# Pre-requisites
To run the converter script you need to have the following installed:

- [Python 3](https://www.python.org/)

The script uses the following Python3 libraries:
- pandas
- numpy

# Getting Started
1. Complete the 'FAIR_Metadata_Template.xlsx' Excel spreadsheet with metadata for your dataset.
2. Run the fair_metadata_converter.py script with the following arguements:
-i <path_to_excel>
-i <output_filename>

For example:
```sh
python3 fair_metadata_converter.py -i FAIR_Metadata_Template.xlsx -o dataset_json.json
```

# Feedback
Contact Gary McGilvary (gary.mcgilvary@aridhia.com) to provide feedback




