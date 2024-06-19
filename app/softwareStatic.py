import pandas as pd
import os
from app.parseVersionInfo import addVersionInfoToTable

staticTable = './staticSearch/staticTable.csv'

# Hard-coded links to RP-specific Software Documentation
rp_urls = {
    'Aces':'https://hprc.tamu.edu/software/aces/',
    'Anvil': 'https://www.rcac.purdue.edu/software/',
    'Bridges-2': 'https://www.psc.edu/resources/software/',
    'DARWIN': 'https://docs.hpc.udel.edu/software/',
    'Delta': 'https://docs.ncsa.illinois.edu/systems/delta/en/latest/user_guide/software.html',
    'Expanse':'https://www.sdsc.edu/support/user_guides/expanse.html#modules',
    'Faster':'https://hprc.tamu.edu/software/faster/',
    'Jetstream2':'',
    'Kyric':'',
    'Ookami':'https://www.stonybrook.edu/commcms/ookami/support/faq/software_on_ookami',
    'Rockfish':'',
    'Stampede-2':'https://tacc.utexas.edu/use-tacc/software-list/',
    'Stampede3':'https://tacc.utexas.edu/use-tacc/software-list/',
    'Ranch':'https://tacc.utexas.edu/use-tacc/software-list/',
    'OSG':'',
    'OSN':''
}
# Some RPs generate specific links to individual software in their documentation.
# Here, for the RPs that do this, we're using an algorithm to point to their
#   specific software pages.


#################################################################
#   createFullDocUrl                                            #
#       Generates RP-specific documentation links for the table #
#       Args:                                                   #
#           softwareName: software as it appears on the table   #
#           rpNames: list of RPs with the software installed    #
#       Return:                                                 #
#           combinedUrls: string of formatted RP URLs           #
#################################################################
def createFullDocUrl(softwareName, rpNames):
    has_individual_software_page = ['Anvil','Bridges-2','DARWIN']   # RPs that have specific links per software
    rpList = rpNames.split(',')                                     # For software installed on multiple systems,
                                                                    #   split the RPs into a list for processing

    urls=[]
    for rp in rpList:
        rpName = rp.strip()                 # Strip off any whitespace 
        rpUrl = rp_urls.get(rpName)         # Grab URL from rp_urls dictionary based on rpName

        # For software with specific links
        if rpName in has_individual_software_page:        
            fullUrl = f"{rpName}: {rpUrl}{softwareName.lower()}"  # fullURL = rpName: rpUrl/softwareName
            
            # Extra Code for DARWIN links, which aren't constructed normally
            if rpName == 'DARWIN':
                fullUrl = f"{fullUrl}/{softwareName.lower()}"     # fullURL = rpName: rpUrl/softwareName/softwareName
        
        # For software from RPs with only generic documentation
        elif rpUrl:
            fullUrl = f"{rpName}: {rpUrl}"
        
        # For software from RPs with no documentation at all
        else:
            fullUrl=''
        
        # Combine URLs across multiple RPs
        if fullUrl:
            urls.append(fullUrl)

    # Format URLs so each is on a separate line in the table cell
    combinedUrls = ' \n'.join(urls)
    return combinedUrls

##################################################################
#   create_static_table                                          #
#       Converts our CSV file into a DataFrame ready for HTML    # 
#       Functions:                                               #
#           createFullDocURL: Populate RP Documentation Cells    #
#           addVersionInfoToTable: Add Version info to DataFrame #
#       Return:                                                  #
#           df: Pandas DataFrame of completed Static Table       #
##################################################################
def create_static_table():
    # If the static table already exists, it doesn't get updated when change it unless we delete it first
    # The app has a cached version. We should decide if we want this behavior or not.
    if os.path.exists(staticTable):
        os.remove(staticTable)

    df = pd.read_csv('./staticSearch/ACCESS_Software.csv',na_filter=False)  # CSV generated from Google Sheets

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
    df.to_csv(staticTable,index=False)
    
    # Export DataFrame to App
    return(df)




# I'm pretty sure this doesn't do anything but I'll wait one update before removing it.
#if __name__ == "__main__":
#    df = create_static_table()