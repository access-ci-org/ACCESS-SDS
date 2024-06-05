from models import db
from models.software_name import SoftwareName
from models.links import Links
from models.pathing import Pathing
import pandas as pd
import sys

def recreate_tables():

    """
    delete and recreate all of the tables in the database
    """
    db.connect(reuse_if_open=True)
    
    with db.atomic() as transaction:
        try:
            tables = db.get_tables()
            print(f"Dropping tables: {tables}")
            db.drop_tables([SoftwareName,Links])

            db.create_tables([SoftwareName,Links])
            tables = db.get_tables()
            print(f"Recreated tables: {tables}")
        except Exception as e:
            transaction.rollback()
            print(e)

    db.close()


def insert_data():

    """
    Adds the data from ACCESS_Software.csv to the SQLlite database
    """

    csv_file_path = 'staticSearch/ACCESS_Software.csv'
    access_software = pd.read_csv(csv_file_path)

    # Ensure column names match the expected format
    expected_columns = [
        'Software', 'RP Name', 'Software Type', 'Software Class', 'Research Area', 'Research Discipline',
        'Software Description', "Software's Web Page", 'Software Documentation/Link',
        'Example Software Use (link)', 'Area-specific Examples', 'Containerized Version of Software',
        'RP Documentations for Software', 'Pathing'
    ]

    if list(access_software.columns) != expected_columns:
        print("CSV columns do not match the expected format.")
        return

    db.connect(reuse_if_open=True)

    with db.atomic() as transaction:
        try:
            print("Adding Software Names and Links to the database")
            for index, row in access_software.iterrows():
                # Debugging print statements to check row data
                print(f"Row {index}: {row.to_dict()}")

                row = row.fillna('')

                # Create SoftwareName entry
                software = SoftwareName.create(
                    software_name=row['Software'],
                    rp_software=row['RP Name'],
                    description=row['Software Description'],
                    software_type=row['Software Type'],
                    software_class=row['Software Class'],
                    research_area=row['Research Area'],
                    research_discipline=row['Research Discipline']
                )

                # Create Links entry
                link = Links.create(
                    website_links=row["Software's Web Page"],
                    documents=row['Software Documentation/Link'],
                    examples=row['Example Software Use (link)'],
                    area_specific=row['Area-specific Examples'],
                    containers=row['Containerized Version of Software'],
                    rp_documents=row['RP Documentations for Software'],


                )
                
                
            # If everything is successful, commit the transaction
            transaction.commit()
            print("Data inserted successfully")
        except Exception as e:
            transaction.rollback()
            print(f"Error in insert_data: {e}")
    
        try:
            # Query the data from the database
            print("Querying data from the database")
            software_data = SoftwareName.select()
            links_data = Links.select()

            # Create DataFrame from the queried data
            software_df = pd.DataFrame(list(software_data.dicts()))
            links_df = pd.DataFrame(list(links_data.dicts()))

            # Combine DataFrames if necessary
            combined_df = pd.concat([software_df, links_df], axis=1)
            
            # Define the output file path
            output_csv_file_path = './staticSearch/staticTable.csv'
            
            # Write the combined DataFrame to a CSV file
            combined_df.to_csv(output_csv_file_path, index=False)
            print(f"Data written to {output_csv_file_path} successfully")
        
        except Exception as e:
            print(f"Here is the error: {e}")
    db.close()


if __name__ == "__main__":

    recreate_tables()
    insert_data()
    print(f"Data inserted")