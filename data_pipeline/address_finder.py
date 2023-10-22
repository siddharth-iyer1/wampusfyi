from googlemaps import Client
import csv
import pandas as pd
from google.cloud import bigquery
import os
import requests

def main():
    PROJECT_ID = "wampusfyi-402717"
    bigquery_client = bigquery.Client(project=PROJECT_ID)

    APT_TABLE_ID = "wampusfyi-402717.DistanceData.AptAddresses"
    PRICES_TABLE_ID = "wampusfyi-402717.FormResponses.RentPrices"

    surveyed_apts = set()
    addressed_apts = set()

    for row in bigquery_client.list_rows(PRICES_TABLE_ID):
        surveyed_apts.add(row["Where_are_you_living_this_year_"])

    for row in bigquery_client.list_rows(APT_TABLE_ID):
        addressed_apts.add(row["Apartment"])

    # Find any apartments in surveyed set that don't exist in addressed set
    diff = surveyed_apts.difference(addressed_apts)
    print(diff)
    diff = [apt.strip() for apt in diff]

    # Then use Google Places API to find the address of the apartment and add it to the table
    for apt in diff:
        # Google Maps API Key
        api_key = "AIzaSyDoPCPo-aK28JSPXhMRHBdzL8jCpjrpvfc"
        client = Client(api_key)
        search_input = apt + " UT West Campus Apartment"

        endpoint_url = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json"
        params = {
            "input": search_input,
            "inputtype": "textquery",
            "fields": "place_id,formatted_address",
            "key": api_key
        }
        response = requests.get(endpoint_url, params=params)
        data = response.json()
        # Extract address
        if data.get('candidates'):
            address = data['candidates'][0].get('formatted_address')
            # Write to apartment addresses csv
            with open('apartment_data/apt_addresses.csv', 'a') as f:
                writer = csv.writer(f)
                writer.writerow([apt, address])
                print('updated!')

    # Now upload the csv to BigQuery

    dataset_ref = bigquery_client.dataset("DistanceData")
    table_ref = dataset_ref.table("AptAddresses")
    csv_file_path = "apartment_data/apt_addresses.csv"

    # Define the job configuration
    job_config = bigquery.LoadJobConfig()
    job_config.source_format = bigquery.SourceFormat.CSV
    job_config.skip_leading_rows = 1  # Assuming the CSV has a header row
    schema = [
        bigquery.SchemaField("Apartment", "STRING", mode="NULLABLE", description="Start Location"),
        bigquery.SchemaField("Address", "STRING", mode="NULLABLE", description="End Location"),
    ]
    job_config.schema = schema

    # Load the CSV into BigQuery
    with open(csv_file_path, "rb") as csv_file:
        job = bigquery_client.load_table_from_file(
            csv_file, table_ref, job_config=job_config
        )
        print('woah!!')


# Make this file runnable in another python file
if __name__ == "__main__":
    main()