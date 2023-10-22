import requests
import googlemaps
import pandas as pd
import json

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

file_path = '/Users/nihalkyasa/Documents/Other/wampusfyi/distance_data/apartment_addresses.csv'
apartment_addys = pd.read_csv(file_path)

gmaps = googlemaps.Client(key=api_key)
reviews_api = GooglePlaces(api_key)

ratings_col = []
reviews_col = []

for idx, row in apartment_addys.iterrows():
    apt = row['Apartment']
    print(apt)
    
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

print(apartment_addys)
    




'''
def get_place_details(place_id, api_key):
    # Send request by API
    response = requests.get(
        f'https://maps.googleapis.com/maps/api/place/details/json?placeid={place_id}&key={api_key}')
    # Read response as json
    resp_details = response.json()
    # status=OK: the place was successfully detected and at least one result was returned
    for i in range(len(resp_details)):

        if resp_details['status'] == 'OK':
            for i in range(len(resp_details)):
                review_rating = resp_details['result']['reviews'][i]['rating']
                review_time = resp_details['result']['reviews'][i]['relative_time_description']
                review_timestamp = resp_details['result']['reviews'][i]['time']
                review_text = resp_details['result']['reviews'][i]['text']
                return [place_id, review_rating, review_time, review_timestamp, review_text]
        else:
            print('Failed to get json response:', resp_details)
            return ['Review is not found', place_id]



api_key = 'AIzaSyDoPCPo-aK28JSPXhMRHBdzL8jCpjrpvfc'

file_path = '/Users/nihalkyasa/Documents/Other/wampusfyi/distance_data/apartment_addresses.csv'
apartment_addys = pd.read_csv(file_path)

gmaps = googlemaps.Client(key=api_key)
place_ids = []
all_reviews = []

for idx, row in apartment_addys.iterrows():
    address = row['Address']

    place_result = gmaps.places(address)
    place_id = place_result['results'][0]['place_id']

    print(get_place_details(place_id, api_key))
    break

    # place_ids.append(place_id)

    
    url = f'https://maps.googleapis.com/maps/api/place/details/json?placeid={place_id}&key={api_key}'
    response = requests.get(url)
    data = response.json()

    print(data['result'])

    reviews = data['result'].get('reviews', [])
    
    all_reviews.append(reviews)
    

    place = gmaps.place(place_id = place_id)

    reviews = place.get('result', {}).get('reviews', [])
    print(place_id)
    print(place)
    print(reviews)
    break

apartment_addys['place_id'] = place_ids
print(apartment_addys)
'''