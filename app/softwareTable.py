import json
import glob
import os
import pandas as pd

from parseJSONInfo import jsonSanitizer
from parseVersionInfo import addVersionInfoToTable
from softwareStatic import createFullDocUrl

CURATED_INPUT_DIRECTORY = './static/data/ACCESS_Software.csv'
CURATED_OUTPUT_DIRECTORY = './static/data/staticTable.csv'

GENERATED_INPUT_DIRECTORY = "./dynamicSearch/software_all_json"
GENERATED_OUTPUT_DIRECTORY = './static/data/generatedTable.csv'

FINAL_OUTPUT_DIRECTORY = './static/data/softwareTable.csv'
JSON_keys = ['Software', 'AI Description', 'Core Features', "General Tags"]


##################################################################
#   createGeneratedTable                                         #
##################################################################
def createSoftwareTable():
    #os.remove(STATIC_OUTPUT_DIRECTORY)
    #os.remove(GENERATED_OUTPUT_DIRECTORY)

    staticTableDF = createStaticTable()
    generatedTableDF = createGeneratedTable()

    mergedDF = staticTableDF.merge(generatedTableDF, how='left', on='Software')
    mergedDF.to_csv(FINAL_OUTPUT_DIRECTORY,index=False)

    return mergedDF


##################################################################
#   createStaticTable                                            #
#       Converts our CSV file into a DataFrame ready for HTML    # 
#       Functions                                                #
#           createFullDocURL: Populate RP Documentation Cells    #
#           addVersionInfoToTable: Add Version info to DataFrame #
#       Return:                                                  #
#           df: Pandas DataFrame of completed Static Table       #
##################################################################
def createStaticTable():
    df = pd.read_csv(CURATED_INPUT_DIRECTORY,na_filter=False)  # CSV generated from Google Sheets

    # Ensure uniform capitalization across cells
    df['RP Name'] = df['RP Name'].str.title()
    df['Software Type'] = df['Software Type'].str.title()
    df['Software Class'] = df['Software Class'].str.title()
    df['Research Area'] = df['Research Area'].str.title()
    df['Research Discipline'] = df['Research Discipline'].str.title()

    # Ensure DARWIN is always capitalized
    df['RP Name'] = df['RP Name'].str.replace('darwin', 'DARWIN')

    # Table Column Formatting
    df.rename(columns={'Software Documentation/Link' : 'Software Documentation'}, inplace=True)
    df.rename(columns={'Example Software Use (link)' : 'Example Software Use'}, inplace=True)

    # Description Source Formatting
    df['Software Description'] = df['Software Description'].str.replace('Description Source:', 
                                                                        '\nDescription Source: ')

    # Make Example Links on separate lines
    df['Example Software Use'] = df['Example Software Use'].str.replace(' , ', ' \n')

    # Populate 'RP Software Documentation' Field
    df['RP Software Documentation'] = df.apply(lambda row: createFullDocUrl(row['Software'], row['RP Name']), axis=1)

    # This really needs to be fixed. If we don't want these columns, get rid of them. If we do, populate them.
    empty_columns = ['Area-specific Examples', 'Containerized Version of Software',
                     'RP Documentations for Software', 'Pathing']
    df.drop(empty_columns,axis=1,inplace=True)
    
    # Add Version Info to DataFrame
    df = addVersionInfoToTable(df)
    df['Version Info'] = df['Version Info'].str.title()

    # Convert DataFrame back to CSV
    df.to_csv(CURATED_OUTPUT_DIRECTORY,index=False)
    
    # Export DataFrame to App
    return(df)


##################################################################
#   createGeneratedTable                                         #
##################################################################
def createGeneratedTable():
    softwareDict = {}
    # Stage the JSON Directory 
    for file in glob.glob(os.path.join(GENERATED_INPUT_DIRECTORY, '*.json')):
        # Filter out improperly created or fragmented JSON objects
        # These are usually due to some random text we added to filter them out intentionally
        # This way they don't break the entire script
        try:
            # Check if JSON has been formatted properly  
            for key in JSON_keys:
                with open(file, 'r') as infile:
                    data = json.load(infile)
                if key in data.keys():
                    continue
                else:
                    jsonSanitizer(file)

        except:
            print("Error reading: " + file)
            continue

        # Stage JSON data to be added to dictionary
        softwareName = data['Software'].lower()
        
        # Additional overhead for specific file(s)
        # Thanks Ookami
        if softwareName == '7-zip':     
            softwareName = '7z'
            data['Software'] = '7z'
        
        # Add JSON data to dictionary
        softwareDict[softwareName] = data

    # Alphabetizes the dictionary, mostly for user friendly CSV generation
    # Easier to make sure the CSV is doing what we want this way
    sortedDict = dict(sorted(softwareDict.items()))

    # Create the DataFrame
    df = pd.DataFrame.from_dict(sortedDict, orient='index', columns=['Software', 'AI Description', 'Core Features', 'General Tags', 'Software Type', 'Software Class', 'Research Field', 'Reserarch Area', 'Research Discipline'], )
    # Ensure uniformity in Software names, since this will be the index
    df['Software'] = df['Software'].str.lower()
    df.set_index('Software', inplace=True)
    # Generate a CSV to 'cache' this information
    df.to_csv(GENERATED_OUTPUT_DIRECTORY)

    return df


createSoftwareTable()