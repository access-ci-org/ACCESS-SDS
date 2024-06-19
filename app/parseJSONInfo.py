import json

nested_key_path = [
    'overview', 
    'comprehensive_overview', 
    'Comprehensive Overview', 
    'comprehensive overview'
    ]

software_names = [
    'tool', 
    'software_name', 
    'software name', 
    'Software Name', 
    'software'
    ]

overview_names = [
    'overview', 
    'comprehensive_overview', 
    'Comprehensive Overview', 
    'comprehensive overview'
    ]

features_names = [
    'core features', 
    'Core Features', 
    'core_features'
    ]

gen_tag_names = [
    'general tags', 
    'General Tags', 
    'general_tags'
    ]

add_tag_names = [
    'additional tags', 
    'Additional Tags', 
    'additional_tags'
    ]

additional_tags_to_fix = [
    'software_type',
    'software_class',
    'research_field',
    'research_area',
    'research_discipline',
    'field_of_science'
    ]

#########################################################
#   jsonSanitizer                                       #
#       Converts AI-generated JSON software files       #
#       into a uniform format for further manipulation  #
#       Parameters:                                     #
#           file: the file to be formatted              #
#########################################################
def jsonSanitizer(file):
    fileName = file.split('json/')[1]
    print("Sanitizing file: " + fileName)

    # Open JSON File
    with open(file, 'r') as infile:
        data = json.load(infile)
    
    # This is the structure we want by the end:
    #{
    #   Software: {}
    #   AI Description: {}
    #   Core Features: {}
    #   General Tags: {}
    #   Software Type: {}
    #   Software Class: {}
    #   Research Field: {}
    #   Research Area: {}
    #   Research Discipline: {}
    #}

    ###########################################
    # 1) Check if the data we want is nested  #
    ###########################################
    # Search for nested tags
    # If found, move everything out of the nest and purge the old structure
    #print("1: Checking JSON structure")
    software_name = list(data.keys())[0]   
    for key in nested_key_path:
        if key in data[software_name]:
            data['Software'] = software_name.lower()
            #print("software_name moved!")

            for key in data[software_name]:
                data[key] = data[software_name][key]
                #print(key + " moved!")

            data.pop(software_name)
            #print("Unpacking complete!")

            # Save the file and exit the loop
            with open(file, 'w') as infile:
                json.dump(data, infile, indent=4)
                break
    
    ############################################################
    # 2) Standardize the tags that exist into a uniform format #
    ############################################################
    #print("2: Checking JSON keys")

    #print("Checking software name...")
    # Check 'Software'
    for sError in software_names:
        if sError in data:
            data['Software'] = data.pop(sError)
            #print("Software name fixed!")      

    #print("Checking description...")
    # Check 'AI Description'
    for oError in overview_names:
        if oError in data.keys():
            data['AI Description'] = data.pop(oError)
            #print("Overview name fixed!")

    #print("Checking core features...")
    # Check 'Core Features'
    for fError in features_names:
        if fError in data:
            data['Core Features'] = data.pop(fError)
            #print("Features fixed!")

    #print("Checking general tags...")
    # Check 'General Tags'
    for tError in gen_tag_names:
        if tError in data:
            data['General Tags'] = data.pop(tError)
            #print("General tags fixed!")
    
    # Capitalize tags for better searching
    count = 0
    for gTag in data['General Tags']:
        gTag = gTag.title()
        data['General Tags'][count] = gTag
        count = count + 1

    # Check for 'Additional Tags'
    # These tend to get nested, but we want them loose to display them more easily in the table
    # If a particular one doesn't exist, create it as a blank field
    
    # Remove tags from 'Additional Tags' nest
    #print("Checking additional tags...")

    for aError in add_tag_names:
        #print(aError)
        if aError in data:
            for tag in additional_tags_to_fix:
                if tag in data[aError]:
                    data[tag] = data[aError][tag] 
                    data[aError].pop(tag)
                else:
                    data[tag] = ""
            data.pop(aError)
           
    # Sanitize tag names and contents
    for tag in additional_tags_to_fix:
        # Check for empty or null list, which will break things later on
        if tag not in data or data[tag] == [] or data[tag] is None:
                data[tag] = ""
        if tag in data:
            match tag:
                case 'software_type':
                    data['Software Type'] = data.pop('software_type')
                    tag = 'Software Type'
                case 'software_class':
                    data['Software Class'] = data.pop('software_class')
                    tag = 'Software Class'
                case 'research_field':
                    data['Research Field'] = data.pop('research_field')
                    tag = 'Research Field'
                case 'field_of_science':
                    if 'Research Field' not in data or data['Research Field'] == "":
                            data['Research Field'] = data.pop('field_of_science')
                    else:
                        data.pop('field_of_science')
                    tag = 'Research Field'
                case 'research_discipline':
                    data['Research Discipline'] = data.pop('research_discipline')
                    tag = 'Research Discipline'
                case 'research_area':
                    data['Research Area'] = data.pop('research_area')
                    tag = 'Research Area'
            
            if isinstance(data[tag], list):
                count = 0
                for subtag in data[tag]:
                    subtag = subtag.title()
                    data[tag][count] = subtag
                    count = count + 1
            else:
                data[tag] = data[tag].title()
            
            if "And" in data[tag]:
                data[tag] = data[tag].replace("And", "&")

    # Save updated JSON file
    with open(file, 'w') as infile:
        json.dump(data, infile, indent=4)
    #print("Formatting complete!")