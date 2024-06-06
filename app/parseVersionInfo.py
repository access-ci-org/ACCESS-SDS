import re
import pandas as pd


rpNames = [
    'aces', 'anvil', 'bridges-2', 'DARWIN', 'delta', 'expanse', 'faster', 'jetstream', 'kyric', 'ookami', 'stampede-3'
]

# Skip RPs that don't currently have spider outputs
skipped_rps = {'DARWIN','ookami','stampede-3'}


#################################################################
#   parseVersionInfo                                            #
#       Converts a module_spider line into a formatted tuple    #
#       Args:                                                   #
#           line: single line taken from a module_spider file   #
#       Return:                                                 #
#           software: software name                             #
#           versions: cleaned up version information as a list  #
#################################################################
def parseVersionInfo(line):
    
    software, versions = line.split(": ")               # Split the input into two parts for processing
    pattern = re.compile(rf'{re.escape(software)}/')    # 'Compile' the software name plus '/' as a regex pattern
    versions = pattern.sub('', versions)                # 'Substitute' the pattern for an empty string
    software = software.split("/")[0].lower()           # Make software uniformly lowercase. Important later,
                                                        #   once we start merging them together
    
    return software, versions


#####################################################################
#   spiderToDictionary                                              #
#       Creates a Dictionary from a module_spider file              #
#       Args:                                                       #
#           input_file: single module_spider file                   #
#       Functions:                                                  #
#           parseVersionInfo: Processing for each line of the file  #
#       Return:                                                     #
#           versionInfoDict: Dictionary of software:version tuples  #           
#####################################################################
def spiderToDictionary(input_file):
    versionInfoDict = {}
    with open(input_file, 'r') as infile:
        for line in infile:
            if (re.match(r'^ {2}(?!\s)', line)):                    # Find Lines that start with two white spaces, 
                                                                    #   which is how module_spider is formatted
                software, versions = parseVersionInfo(line.strip()) # Strip off whitespace from tuple
                versionInfoDict[software] = versions                # Add tuple to dictionary
        infile.close()
        return versionInfoDict


#####################################################################
#   generateRPDictionaries                                          #
#       Creates a Dictionary of RP Software Dictionaries            #
#       Functions:                                                  #
#           spiderToDictionary: Create individual RP Dictionaries   #
#       Return:                                                     #
#           rpDict: Dictionary -> {RP Name:RP Dictionary}           #
#####################################################################
def generateRPDictionaries():
    rpDict = {}
    for rpName in rpNames:                                                  # For each RP
        if rpName in skipped_rps:                                           # Skip RPs without module_spider configured
            continue
        else:
            fileName = "./spiderOutput/" + rpName + "_spider_output.txt"    # Find module_spider file
            rpDict[rpName] = spiderToDictionary(fileName)                   # Store RP Dictionary under RP Name
    return rpDict


#####################################################################
#   convertRPDictToDataFrame                                        #
#       Convert Combined RP Dictionary to Pandas DataFrame          #
#       Functions:                                                  #
#           generateRPDictionaries: Create Dictionary per RP        #
#       Return:                                                     #
#           df: DataFrame with Combined Version Info                #
#####################################################################
def convertRPDictToDataFrame():
    combinedVIDict = {}
    rpVIDict = generateRPDictionaries()

    # Combine Dictionaries together to be added to DataFrame
    for rpName in rpNames:
        if rpName in skipped_rps:
            continue
        else:
            # For each software in each RP Dictionary
            for software in rpVIDict[rpName]:
                rpVersionInfo = rpName + ": " + rpVIDict[rpName].get(software) # Formatted String
                # If software key already exists in dictionary, append RP Version Info to the same key
                #   otherwise, key is overwritten by most-recent value
                if software in combinedVIDict:
                    combinedVIDict[software] = combinedVIDict[software] + "\n" + rpVersionInfo
                else:   
                    combinedVIDict[software] = rpVersionInfo
    
    # Create DataFrame from Combined Dictionary
    df = pd.DataFrame.from_dict(combinedVIDict, orient='index', columns=['Version Info'])
    df.index.name = 'Software'                              # Define Index of DataFrame
    df.reset_index(inplace=True)                            # Include Index in DataFrame
    df.to_csv('./staticSearch/versionInfo.csv',index=False) # Write DataFrame to CSV (Testing Purposes)
    return df


#############################################################################
#   addVersionInfoToTable                                                   #
#       Add Combined RP Version Info DataFrame to Static DataFrame          #
#       Args:                                                               #
#           static_df: DataFrame from Static Table                          #
#       Functions:                                                          #
#           convertRPDictToDataFrame: Create DataFrame from RP Dictionary   #
#       Return:                                                             #
#           merged_df: Static DataFrame merged with Version Info DataFrame  #
#############################################################################
def addVersionInfoToTable(static_df):
    version_df = convertRPDictToDataFrame()
    merged_df = static_df.merge(version_df, how='left', on='Software')  # 'Left' Join returns all rows from static_df
                                                                        #   and adds version_df to them based on the
                                                                        #   matching 'Software' column in both
    return merged_df




### IGNORE #######################################################
# Implementation for outputting to a text file instead of a dict #
# In case we ever want this in the future                        #
##################################################################
'''
input_files = {Put Input Files Here}
output_file = 'Put Output File Here'

# Output to a .txt File
def processVersionInfo(input_files, output_file):
    processed_lines = set()
    with open(output_file, 'w') as outfile:
        for input_file in input_files:
            with open(input_file, 'r') as infile:
                for line in infile:
                    if (re.match(r'^ {2}(?!\s)', line)):    # Find Lines that start with two white spaces, 
                                                            # which is currently how this file is formatted
                        processed_line = parseVersionInfo(line.strip())
                        if processed_line not in processed_lines:                            
                            outfile.write(processed_line + '\n')
                            processed_lines.add(processed_line)


# Parse Version Numbers into CSV-Usable Text
def parseVersionInfo(line):
    
    software, versions = line.split(": ")               # Select everything before the colon as the pattern
    pattern = re.compile(rf'{re.escape(software)}/')    # 'Compile' the software name + / as a regex pattern
    versions = pattern.sub('', versions)                # 'Substitute' software name for an empty string
    versions = re.sub(r', ', ',', versions)             # Trim white space between versions
    
    return f"{software}:{versions.strip()}"

# Testing, Deletes output_file first before running
if os.path.exists(output_file):
    os.remove(output_file)
processVersionInfo(input_files, output_file)
'''