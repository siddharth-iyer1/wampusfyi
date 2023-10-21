import requests
import googlemaps

api_key = 'AIzaSyDoPCPo-aK28JSPXhMRHBdzL8jCpjrpvfc'
address = '1600 Amphitheatre Parkway, Mountain View, CA'

gmaps = googlemaps.Client(key=api_key)
place_result = gmaps.places(address)
place_id = place_result['results'][0]['place_id']
print(place_id)

'''
url = f'https://maps.googleapis.com/maps/api/place/details/json?placeid={place_id}&key={api_key}'
response = requests.get(url)
data = response.json()
'''
