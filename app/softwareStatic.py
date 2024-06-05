import pandas as pd


rp_urls={
    'aces':'https://hprc.tamu.edu/software/aces/',
    'anvil': 'https://www.rcac.purdue.edu/software/',
    'bridges-2': 'https://www.psc.edu/resources/software/',
    'darwin': 'https://docs.hpc.udel.edu/software/',
    'delta': 'https://docs.ncsa.illinois.edu/systems/delta/en/latest/user_guide/software.html',
    'expanse':'https://www.sdsc.edu/support/user_guides/expanse.html#modules',
    'faster':'https://hprc.tamu.edu/software/faster/',
    'jetstream2':'',
    'kyric':'',
    'ookami':'https://www.stonybrook.edu/commcms/ookami/support/faq/software_on_ookami',
    'rockfish':'',
    'stampede-2':'https://tacc.utexas.edu/use-tacc/software-list/',
    'stampede3':'https://tacc.utexas.edu/use-tacc/software-list/',
    'ranch':'https://tacc.utexas.edu/use-tacc/software-list/',
    'osg':'',
    'osn':''
}

def create_full_url(rp_names, software_name):
    has_individual_software_page = ['anvil','bridges-2','darwin']
    rp_names_list = rp_names.split(',')

    urls=[]
    for rp_name in rp_names_list:
        rp_name_l = rp_name.strip().lower()
        base_url = rp_urls.get(rp_name_l,'')

        if rp_name_l in has_individual_software_page and base_url:
            full_url=f"{rp_name}: {base_url}{software_name.lower()}"
            if rp_name_l == 'darwin':
                full_url=f"{full_url}/{software_name.lower()}"
        elif base_url:
            full_url = f"{rp_name}: {base_url}"
        else:
            full_url=''
        
        if full_url:
            urls.append(full_url)

    combined_urls = ' \n'.join(urls)
    return combined_urls

def create_static_table():
    df = pd.read_csv('./staticSearch/staticTable.csv',na_filter=False)
    df['rp_documents'] = df.apply(lambda row: create_full_url(row['rp_software'],row['software_name']), axis=1)
    empty_columns_plus_id = ['id', 'id.1']
    
    df.drop(empty_columns_plus_id,axis=1,inplace=True)
    df.to_csv('./staticSearch/staticTable.csv',index=False)
    return(df)

if __name__ == "__main__":
    df = create_static_table()