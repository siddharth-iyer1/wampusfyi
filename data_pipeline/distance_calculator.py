from googlemaps import Client
import csv
import pandas as pd
from google.cloud import bigquery
import os
def main():
    # Takes CSV files of Addresses of Apartments and Colleges at UT and returns a CSV of distances between all combinations

    # Google Maps API Key
    api_key = "AIzaSyDoPCPo-aK28JSPXhMRHBdzL8jCpjrpvfc"
    client = Client(api_key)

    # GCP Big Query Client
    PROJECT_ID = "wampusfyi-402717"
    bigquery_client = bigquery.Client(project=PROJECT_ID)

    # Locations of CSV files
    APT_TABLE_ID = "wampusfyi-402717.DistanceData.AptAddresses"
    CLG_TABLE_ID = "wampusfyi-402717.DistanceData.ClgAddresses"

    # List rows from the table and convert to DataFrame
    apt_rows = bigquery_client.list_rows(APT_TABLE_ID)
    apt_df = apt_rows.to_dataframe()
    clg_rows = bigquery_client.list_rows(CLG_TABLE_ID)
    clg_df = clg_rows.to_dataframe()

    # Upload coordinates to a table in the csv file
    geocode_result = []
    for i in apt_df["Address"]:
        geocode_result.append(client.geocode(i))
    apt_df['coords'] = geocode_result

    geocode_result = []
    for i in clg_df["Address"]:
        geocode_result.append(client.geocode(i))
    clg_df['coords'] = geocode_result

    distance_df = pd.DataFrame(columns=['Apartment', 'School', 'Distance'])

    for i in range(len(apt_df)):
        apt_lat = apt_df['coords'][i][0]['geometry']['location']['lat']
        apt_lng = apt_df['coords'][i][0]['geometry']['location']['lng']
        for j in range(len(clg_df)):
            college_lat = clg_df['coords'][j][0]['geometry']['location']['lat']
            college_lng = clg_df['coords'][j][0]['geometry']['location']['lng']
            distance = client.distance_matrix((apt_lat, apt_lng), (college_lat, college_lng), mode="walking")['rows'][0]['elements'][0]['distance']['text']
            # Convert km to miles
            distance = round((float(distance.split(" ")[0]) * 0.621371), 2)

            # Add distance to df
            new_row = pd.DataFrame({
                'Apartment': [apt_df['Apartment'][i]],
                'School': [clg_df['College'][j]],
                'Distance': [distance]
            })

            distance_df = pd.concat([distance_df, new_row], ignore_index=True)

    distance_df.to_csv('apartment_data/distance_data.csv', index=False)

    # Now upload the csv to BigQuery

    dataset_ref = bigquery_client.dataset("DistanceData")
    table_ref = dataset_ref.table("Distances")
    csv_file_path = "apartment_data/distance_data.csv"

    # Define the job configuration
    job_config = bigquery.LoadJobConfig()
    job_config.source_format = bigquery.SourceFormat.CSV
    job_config.skip_leading_rows = 1  # Assuming the CSV has a header row
    schema = [
        bigquery.SchemaField("Apartment", "STRING", mode="NULLABLE", description="Start Location"),
        bigquery.SchemaField("College", "STRING", mode="NULLABLE", description="End Location"),
        bigquery.SchemaField("Distance", "FLOAT", mode="NULLABLE", description="Distance between locations"),
    ]
    job_config.schema = schema

    # Load the CSV into BigQuery
    with open(csv_file_path, "rb") as csv_file:
        job = bigquery_client.load_table_from_file(
            csv_file, table_ref, job_config=job_config
        )


# Make this file runnable in another python file
if __name__ == "__main__":
    main()