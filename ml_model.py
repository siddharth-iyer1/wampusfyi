import requests
import googlemaps
import pandas as pd

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

    '''
    url = f'https://maps.googleapis.com/maps/api/place/details/json?placeid={place_id}&key={api_key}'
    response = requests.get(url)
    data = response.json()

    print(data['result'])

    reviews = data['result'].get('reviews', [])
    
    all_reviews.append(reviews)
    '''

    place = gmaps.place(place_id = place_id)

    reviews = place.get('result', {}).get('reviews', [])
    print(place_id)
    print(place)
    print(reviews)
    break

apartment_addys['place_id'] = place_ids
print(apartment_addys)
