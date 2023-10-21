from googlemaps import Client
import csv
import pandas as pd

"""
apartments = csv.DictReader(open('/Users/siddharthiyer/Documents/GitHub/wampusfyi/distance_data/apartment_addresses.csv'))
colleges = csv.DictReader(open('/Users/siddharthiyer/Documents/GitHub/wampusfyi/distance_data/college_addresses.csv'))
"""
api_key = "AIzaSyDoPCPo-aK28JSPXhMRHBdzL8jCpjrpvfc"
client = Client(api_key)

apt_df = pd.read_csv("distance_data/apartment_addresses.csv")
college_df = pd.read_csv("distance_data/college_addresses.csv")

# Upload coordinates to a table in the csv file
geocode_result = []
for i in apt_df["Address"]:
    geocode_result.append(client.geocode(i))
apt_df['coords'] = geocode_result

geocode_result = []
for i in college_df["Address"]:
    geocode_result.append(client.geocode(i))
college_df['coords'] = geocode_result

distance_df = pd.DataFrame(columns=['Apartment', 'School', 'Distance'])

for i in range(len(apt_df)):
    apt_lat = apt_df['coords'][i][0]['geometry']['location']['lat']
    apt_lng = apt_df['coords'][i][0]['geometry']['location']['lng']
    for j in range(len(college_df)):
        college_lat = college_df['coords'][j][0]['geometry']['location']['lat']
        college_lng = college_df['coords'][j][0]['geometry']['location']['lng']
        distance = client.distance_matrix((apt_lat, apt_lng), (college_lat, college_lng), mode="walking")['rows'][0]['elements'][0]['distance']['text']
        # Convert km to miles
        distance = str(round((float(distance.split(" ")[0]) * 0.621371), 2)) + " miles"

        # Add distance to df
        new_row = pd.DataFrame({
            'Apartment': [apt_df['Apartment'][i]],
            'School': [college_df['College'][j]],
            'Distance': [distance]
        })

        distance_df = pd.concat([distance_df, new_row], ignore_index=True)

distance_df.to_csv('distance_data/distance_data.csv', index=False)
