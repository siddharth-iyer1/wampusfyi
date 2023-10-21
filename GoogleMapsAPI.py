from googlemaps import Client

api_key = "AIzaSyDoPCPo-aK28JSPXhMRHBdzL8jCpjrpvfc"

client = Client(api_key)

# Get the latitude and longitude of two points
lat1 = 37.4419
lng1 = -122.1419
lat2 = 37.7750
lng2 = -122.4189

# Calculate the distance between the two points
distance = client.distance_matrix((lat1, lng1), (lat2, lng2))['rows'][0]['elements'][0]['distance']['value']

print(distance)