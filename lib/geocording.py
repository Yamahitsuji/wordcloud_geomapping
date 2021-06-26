import os
import googlemaps

API_KEY = os.getenv('GCP_API_KEY')
client = googlemaps.Client(key=API_KEY)


def get_lat_and_lng(spot_name):
    if spot_name == "":
        return 0, 0
    ls = client.geocode(spot_name)
    if not ls:
        return 0, 0
    return ls[0]["geometry"]["location"]["lat"], ls[0]["geometry"]["location"]["lng"]
