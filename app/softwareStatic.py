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