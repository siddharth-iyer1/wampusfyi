import requests
import googlemaps
import pandas as pd
import json
from google.cloud import bigquery
from googlemaps import Client
import os

# GCP Big Query Client
PROJECT_ID = "wampusfyi-402717"
bigquery_client = bigquery.Client(project=PROJECT_ID)

class GooglePlaces(object):

    def __init__ (self, api_key):
        self.api_key = api_key

    def get_reviews (self, place_id):
        url = f'https://maps.googleapis.com/maps/api/place/details/json?placeid={place_id}&key={self.api_key}'
        params = {
            'placeid': place_id,
            'fields': ['reviews'],
            'key': self.api_key
        }

        res = requests.get(url, params=params)
        place_details = json.loads(res.content)
        return place_details

api_key = 'AIzaSyDoPCPo-aK28JSPXhMRHBdzL8jCpjrpvfc'

file_path = '/Users/nihalkyasa/Documents/Other/wampusfyi/apartment_data/apt_addresses.csv'
apartment_addys = pd.read_csv(file_path)
print(apartment_addys)

gmaps = googlemaps.Client(key=api_key)
reviews_api = GooglePlaces(api_key)

ratings_col = []
reviews_col = []

for idx, row in apartment_addys.iterrows():
    apt = row['Apartment']
    
    # find place_id and plug into reviews api
    place_result = gmaps.places(apt)
    place_id = place_result['results'][0]['place_id']

    place_deets = reviews_api.get_reviews(place_id)

    place_rating = 0
    place_reviews = []

    # add on individual ratings and reviews
    for item in place_deets['result']['reviews']:
        place_rating += item['rating']
        place_reviews.append(item['text'])

    # turn rating into an average
    place_rating /= 5

    # append it to df column
    ratings_col.append(place_rating)
    reviews_col.append(place_reviews)

apartment_addys['rating'] = ratings_col
apartment_addys['reviews'] = reviews_col

apartment_addys.to_csv('apt_addresses_with_reviews.csv', index=False)

# Now upload the csv to BigQuery

dataset_ref = bigquery_client.dataset("ApartmentDetails")
table_ref = dataset_ref.table("Reviews")
csv_file_path = "apt_addresses_with_reviews.csv"

# Define the job configuration
job_config = bigquery.LoadJobConfig()
job_config.source_format = bigquery.SourceFormat.CSV
job_config.skip_leading_rows = 1  # Assuming the CSV has a header row
schema = [
    bigquery.SchemaField("Apartment", "STRING", mode="NULLABLE", description="Apartment Name"),
    bigquery.SchemaField("Address", "STRING", mode="NULLABLE", description="Address of Apt"),
    bigquery.SchemaField("Rating", "FLOAT", mode="NULLABLE", description="Avg Rating"),
    bigquery.SchemaField("Reviews", "RECORD", mode="NULLABLE", description="Google Reviews")
]
job_config.schema = schema

# Load the CSV into BigQuery
with open(csv_file_path, "rb") as csv_file:
    job = bigquery_client.load_table_from_file(
        csv_file, table_ref, job_config=job_config
    )

if os.path.exists("apt_addresses_with_reviews.csv"):
    os.remove("apt_addresses_with_reviews.csv")