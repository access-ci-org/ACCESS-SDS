import json
import glob
import os
import pandas as pd
import numpy as np

from app.parseJSONInfo import jsonSanitizer
from app.parseVersionInfo import addVersionInfoToTable
from app.softwareStatic import createFullDocUrl

CURATED_INPUT_DIRECTORY = './static/data/ACCESS_Software.csv'
CURATED_OUTPUT_DIRECTORY = './static/data/staticTable.csv'

GENERATED_INPUT_DIRECTORY = "./static/JSON"
GENERATED_OUTPUT_DIRECTORY = './static/data/generatedTable.csv'

FINAL_OUTPUT_DIRECTORY = './static/data/softwareTable.csv'

JSON_keys = [
    'Software', 
    'AI Description', 
    'Core Features', 
    'General Tags', 
    'Software Type', 
    'Software Class',
    'Research Field',
    'Research Area',
    'Research Discipline'
    ]

column_order = ['Software', 'RP Name', 'Software Type', 'Software Class', 'Research Field', 'Research Area', 
                'Research Discipline', 'Software Description', 'Core Features', 'General Tags', "Software's Web Page",
                'Software Documentation', 'Example Software Use', 'RP Software Documentation', 'Version Info', 'AI Description', 'Example Use']


##################################################################
#   createGeneratedTable                                         #
##################################################################
def createSoftwareTable():
    mergeColumns = ['Software Type', 'Software Class', 'Research Area', 'Research Discipline']

    # Read cached tables, if they exist
    # Otherwise, recreate as little as necessary
    try:
        mergedDF = pd.read_csv(FINAL_OUTPUT_DIRECTORY)
        print("Software table found!")
    except:
        print("Software table not found. Creating...")
        try:
            staticTableDF = pd.read_csv(CURATED_OUTPUT_DIRECTORY, na_filter=False)
            print("Static Table found!")
        except:
            staticTableDF = createStaticTable()
            print("Static table not found. Creating...")
        try:
            generatedTableDF = pd.read_csv(GENERATED_OUTPUT_DIRECTORY)
            print("AI Generated table found!")
        except:
            generatedTableDF = createGeneratedTable('f')
            print("AI Generated table not found. Creating...")

        # Merge tables by index
        mergedDF = staticTableDF.merge(generatedTableDF, how='left', on='Software', suffixes=('_static', '_generated'))
        mergedDF = mergedDF.replace('', np.nan)
        # Combine matching columns, prioritizing the AI Generated information
        for column in mergeColumns:
            mergedDF[column] = mergedDF[column + '_generated'].combine_first(mergedDF[column + '_static'])
        
        # Drop the unmerged versions of columns
        mergedDF = mergedDF.drop(columns=[column + '_static' for column in mergeColumns] + [column + '_generated' for column in mergeColumns] )
        
        mergedDF.insert(16, 'Example Use', '')

        mergedDF = mergedDF[column_order]
        # Cache the table for efficiency
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
def createGeneratedTable(override):
    softwareDict = {}
    # Stage the JSON Directory 
    for file in glob.glob(os.path.join(GENERATED_INPUT_DIRECTORY, '*.json')):
        # Filter out improperly created or fragmented JSON objects
        # These are usually due to some random text we added to filter them out intentionally
        # This way they don't break the entire script
        try:
            if override.lower() == 't':
                forceRun = True
            else:
                forceRun = False
            # Check if JSON has been formatted properly  
            for key in JSON_keys:
                with open(file, 'r') as infile:
                    data = json.load(infile)
                if key not in data.keys() or forceRun:
                    jsonSanitizer(file)
                    forceRun = False
                    

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
    df = pd.DataFrame.from_dict(sortedDict, orient='index', columns=['Software', 'AI Description', 'Core Features', 'General Tags', 'Software Type', 'Software Class', 'Research Field', 'Research Area', 'Research Discipline'], )
    # Ensure uniformity in Software names, since this will be the index
    df['Software'] = df['Software'].str.lower()
    df.set_index('Software', inplace=True)
    # Generate a CSV to 'cache' this information
    df.to_csv(GENERATED_OUTPUT_DIRECTORY)

    return df


#createSoftwareTable()