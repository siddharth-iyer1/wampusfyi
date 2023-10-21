from googlemaps import Client
import csv
import pandas as pd

"""
apartments = csv.DictReader(open('/Users/siddharthiyer/Documents/GitHub/wampusfyi/distance_data/apartment_addresses.csv'))
colleges = csv.DictReader(open('/Users/siddharthiyer/Documents/GitHub/wampusfyi/distance_data/college_addresses.csv'))
"""
api_key = "AIzaSyDoPCPo-aK28JSPXhMRHBdzL8jCpjrpvfc"
client = Client(api_key)

df = pd.read_csv("C:/Users/sahil/Desktop/CS Files/wampusfyi/distance_data/apartment_addresses.csv")

geocode_result = []

for i in df["Address"]:
        geocode_result.append(client.geocode(i))

df['coords'] = geocode_result

print(df['coords'])

# Get the latitude and longitude of two points
lat1 = 37.4419
lng1 = -122.1419
lat2 = 37.7750
lng2 = -122.4189

# Calculate the distance between the two points
distance = client.distance_matrix((lat1, lng1), (lat2, lng2))['rows'][0]['elements'][0]['distance']['value']

print(distance)


geocode_result = []

for i in range(2):
    geocode_result.append.geocode('1600 Amphitheatre Parkway, Mountain View, CA')

print(geocode_result)