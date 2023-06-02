import requests


def elevation(lon,lat,key_googlemaps):

	url = ("https://maps.googleapis.com/maps/api/elevation/json?locations=" + 
		str(lat) + "%2C" + str(lon) + "&key=" + key_googlemaps)
	try:
		r = requests.get(url).json()
		elevation_value = float(r["results"][0]["elevation"])
	except:
		print("No information on elevation was obtained.")
		elevation_value=0

	return elevation_value
	