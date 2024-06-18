import os
import json
import glob
import pandas as pd
from collections import OrderedDict

INPUT_DIRECTORY = "./dynamicSearch/software_all_json"
OUTPUT_DIRECTORY = './static/data/test.csv'
JSON_keys = {'software_name', 'comprehensive_overview', 'core_features', "general_tags", "additional_tags"}
nested_key_path = ['overview', 'comprehensive_overview']
software_names = {'tool', 'software', 'software name'}
overview_names = {'overview', 'comprehensive_overview', 'Comprehensive Overview'}
features_names = ['core features', 'Core Features']
gen_tag_names = ['general tags', 'General Tags']
add_tag_names = ['additional tags', 'Additional Tags']
additional_tags_to_fix = ['software_type','software_class','research_field','research_area','research_discipline','field_of_science']

def createDynamicTable():
    dict = {}
    for file in glob.glob(os.path.join(INPUT_DIRECTORY, '*.json')):
        try:    
            for key in JSON_keys:
                with open(file, 'r') as infile:
                    data = json.load(infile, object_pairs_hook=OrderedDict)
                if key in data.keys():
                    continue
                else:
                    jsonSanitizer(file)
            softwareName = data['software_name']
            dict[softwareName] = data
        except:
            #print("Error reading: " + file)
            continue
    #print("Sanitizing data... done")

    df = pd.DataFrame.from_dict(dict, orient='index', columns=['software_name', 'comprehensive_overview', 'core_features', 'general_tags'], )
    df.set_index('software_name', inplace=True)
    df.to_csv(OUTPUT_DIRECTORY)
    #print("DataFrame... done")
    return df




########################
def jsonSanitizer(file):
    fileName = file.split('json/')[1]
    #print("Sanitizing file: " + fileName)

    with open(file, 'r') as infile:
        data = json.load(infile, object_pairs_hook=OrderedDict)

    software_name = list(data.keys())[0]
    for key in nested_key_path:
        if key in data[software_name]:
            data['software_name'] = software_name.lower()
            #print("software_name moved!")

            for key in data[software_name]:
                data[key] = data[software_name][key]
                #print(key + " moved!")

            data.pop(software_name)
            #print("Unpacking complete!")
            with open(file, 'w') as infile:
                json.dump(data, infile, indent=4)
            
            jsonSanitizer(file)

    #print("Checking JSON keys!")
        
    #print("Checking software name...")
    for error in software_names:
        if error in data:
            data['software_name'] = data.pop(error)
            #print("Software name fixed!")

    #print("Checking description...")
    for error in overview_names:
        if error in data:
            data['comprehensive_overview'] = data.pop(error)
            #print("Overview name fixed!")

    #print("Checking core features...")
    for error in features_names:
        if error in data:
            data['core_features'] = data.pop(error)
            #print("Features fixed!")

    #print("Checking general tags...")
    for error in gen_tag_names:
        if error in data:
            data['general_tags'] = data.pop(error)
            #print("General tags fixed!")
    
    #print("Checking additional tags...")
    for error in add_tag_names:
        if error in data:
            data['additional_tags'] = data.pop(error)
            #print("Additional tags fixed!")

    if 'additional_tags' not in data:
        #print("Additional Tags Missing!")
        
        data['additional_tags'] = OrderedDict()
        nested_fields = OrderedDict()

        for tag in additional_tags_to_fix:
            if tag in data:
                nested_fields[tag] = data.pop(tag)
        
        data['additional_tags'].update(nested_fields)
        #print("Additional Tags fixed!")
    else:
        data['additional_tags'] = data.pop('additional_tags')

    
    with open(file, 'w') as infile:
        json.dump(data, infile, indent=4)
    #print("Formatting complete!")


#####################################
createDynamicTable()