from random import choice
import string
import googlemaps
from decouple import config
import reverse_geocode
from haversine import haversine, Unit


google_api_key = config('google_api_key')

# function to get code
def event_code(): 

    a = []
    for i in range(8):
        a.append(choice(string.ascii_letters))

    return (''.join(a))




# function to convert an address to latitude and longitude
def latitude_longitude(address, state, country):

    location = address + ', ' + state + ', ' + country 

    try:
        gmaps = googlemaps.Client(key=google_api_key)
        geocode_result = gmaps.geocode(location)
        return (geocode_result[0]['geometry']['location'])


    except:
        return ('This location was not found')


# get address when provided latitude
def getAddress(latitude, longitude):

    coordinates = (latitude, longitude), 

    address = reverse_geocode.search(coordinates)

    return(address)



# Function helps to check distance between two locations
def checkDistance(userLocation, otherLocation, unit='km'):
    
    location_distance = haversine(userLocation, otherLocation, unit)

    return(location_distance)


