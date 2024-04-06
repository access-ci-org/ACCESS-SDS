from confluenceAPI import ConfluenceAPI
import pandas as pd

###
# Used for updating software data from conf
# Get software data from conf, combine the software data from conf and local data
# create new table from combined data
# push table to rp software page
##


def get_local_software(rp_name):

    # TODO: update this function when we don't have fake softwares

    return []

def get_conf_software(conf_api,page_id):

    page_data, page_name = conf_api.get_tabulated_page_data(page_id)
    if "Software" in page_name and "All RP Software" != page_name:
        conf_sftw = page_data[0].iloc[:, 0].dropna().tolist()
        return conf_sftw, page_name

    return None


def combine_software_data(conf_sftw, local_sftw):

    if conf_sftw is None:
        return local_sftw
    
    conf_sftw_set = set(conf_sftw)
    local_sftw_set = set(local_sftw)

    combined_sftw_set = conf_sftw_set.union(local_sftw_set)

    combined_sftw = list(combined_sftw_set)
    print(combined_sftw)
    combined_sftw.sort()

    return combined_sftw

def update_rp_software_page(conf_api, rp_name, page_data):

    title = f"{rp_name} Software"
    body = page_data.to_html(index=False, classes='confluenceTable')

    conf_api.update_or_create_page(title=title, body=body)

if __name__ == '__main__':
    try:
        conf_api = ConfluenceAPI()
        child_page_ids = conf_api.get_page_children_ids()
        print("Updating Conf software pages")
        for id in child_page_ids:
            conf_sftw, page_name = get_conf_software(conf_api=conf_api, page_id=id)
            if conf_sftw:
                rp_name = page_name.split()[0]
                local_sftw = get_local_software(rp_name=rp_name)
                combined_sftw = combine_software_data(conf_sftw=conf_sftw, local_sftw=local_sftw)
                sftw_table = pd.DataFrame({'Software Packages': combined_sftw}).to_html(index=False,classes='confluenceTable')
                conf_api.update_or_create_page(title=page_name,body=sftw_table)
                print(f"{page_name} updated")
            else:
                print(f"Skipping page {page_name}")
            
    except Exception as e:
        print(e)