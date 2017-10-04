from flask import Flask, jsonify
import pyrebase
import math
import json
import uuid
import requests
import datetime
from pytz import timezone, utc
from yelp.client import Client
from yelp.oauth1_authenticator import Oauth1Authenticator
from os import environ
from googleplaces import GooglePlaces, types, lang
from timezonefinder import TimezoneFinder
from geopy.distance import vincenty


YOUR_API_KEY = 'AIzaSyDBghn4IdWKYc8YC2b2N_xYf5eaouqWvtg'

google_places = GooglePlaces(YOUR_API_KEY)

app = Flask (__name__)

yelp_auth = auth = Oauth1Authenticator(
    consumer_key = environ.get("YELP_KEY"),
    consumer_secret = environ.get("YELP_CSECRET"),
    token = environ.get("YELP_TOKEN"),
    token_secret = environ.get("YELP_TSECRET")
)

yelp_client = Client(yelp_auth)

WEATHER_API_KEY = environ.get("WEATHER_KEY")
firebase_config = {
  "apiKey": environ.get("FIREBASE_KEY"),
  "authDomain": environ.get("FIREBASE_NAME") + ".firebaseapp.com",
  "databaseURL": "https://"+environ.get("FIREBASE_NAME") +".firebaseio.com",
  "storageBucket": environ.get("FIREBASE_NAME") + ".appspot.com"
}


firebase = pyrebase.initialize_app(firebase_config)
db = firebase.database()
@app.route('/conditions/<string:lat>/<string:lon>', methods=['GET'])
def get_conditions(lat, lon):
    return []

@app.route('/location_tags/<string:lat>/<string:lon>', methods=['GET'])
def get_location_tags(lat, lon):
    lat = float(lat)
    lon = float(lon)
    conditions = get_current_conditions(lat, lon)
    return jsonify(conditions)

@app.route('/search/<string:cat>', methods=['GET'])
def get_search(cat):
    params = {
        "term": cat,
        "radius_filter" : 500,
        #"limit": 20,
        "sort" : 1, #sort by distance
        #"open_now" : True,
    }
    resp = yelp_client.search_by_coordinates(42.046876, -87.679532, **params)
    info = []
    if not resp.businesses:
        return []
    for b in resp.businesses:
        name = b.name
        name = name.replace(" ", "_")
        categories = [c[1] for c in b.categories]
        info = info  + [name, categories]
    
    return jsonify(info)


def get_current_conditions(lat, lon):
    current_conditions = []
    current_conditions += get_weather(lat, lon)
    current_conditions += yelp_api(lat, lon)
    current_conditions += local_testing_spots(lat, lon)
    #current_conditions += google_api(lat, lon)
    current_conditions = map(lambda x: x.lower(), list(set(current_conditions)))
    
    get_objects(current_conditions)
    print(current_conditions)
    return current_conditions


def get_objects(conditions):
    objects = {"beaches": ["waves", "build_a_sandcastle"], "northwestern_university_library": ["castle"],
               "coffee": ["chair", "sit_in_a_chair"], "parks": ["trees", "grass", "frolick", "hug_a_tree", "pick_a_leaf"], 
               "hackerspace": ["computer", "relax_in_a_chair", "surf_the_interweb"], 
               "trainstations": ["train", "ride_a_train"], "northwestern_university_sailing_center": ["sailboat"],
            }

    for key, value in objects.iteritems():
        if key in conditions: 
            conditions+= value
    return conditions

@app.route('/local_testing/<string:lat>/<string:lon>', methods=['GET'])
def local_testing_spots(lat, lon):
    testing_spots = [{"hackerspace": (42.056929, -87.676694)}, 
                     {"end_of_f_wing": (42.057472, -87.67662)},
                     {"atrium": (42.057323, -87.676164)},
                     {"k_wing": (42.05745, -87.675085)},
                     {"l_wing":(42.057809, -87.67611)},
                     {"grocery": (42.047691, -87.679189)},
                     {"grocery": (42.047691, -87.679189)},
                     {"grocery": (42.047874, -87.679489)}

                     ]

    close_locations = []
    for loc in testing_spots:
        dist = vincenty(loc.values()[0], (lat, lon)).meters
        if( dist < 35):
            print(loc.keys()[0])
            print(dist)
            close_locations.append(loc.keys()[0])
    return close_locations




def get_weather(curr_lat, curr_lon):
    url = "http://api.openweathermap.org/data/2.5/weather?lat=" + str(curr_lat) + "&lon=" + str(curr_lon) + "&appid=" + WEATHER_API_KEY
    response = (requests.get(url)).json()
    weather = response["weather"][0]["main"]
    sunset = datetime.datetime.fromtimestamp(response["sys"]["sunset"])
    sunrise = datetime.datetime.fromtimestamp(response["sys"]["sunrise"])

    sunset_in_utc = sunset.replace(tzinfo=utc)
    sunrise_in_utc = sunrise.replace(tzinfo=utc)
    current_in_utc = datetime.datetime.now().replace(tzinfo=utc)

    tf = TimezoneFinder()
    tz = timezone(tf.timezone_at(lng=curr_lon, lat=curr_lat))
    current_local = current_in_utc.replace(tzinfo=tz)

    if(abs(sunset_in_utc - current_in_utc) <= datetime.timedelta(minutes = 25)):
        return [weather, "SUNSET"]#, current_in_utc, ["sunset", sunset_in_utc]]

    if(abs(sunrise_in_utc - current_in_utc) <= datetime.timedelta(minutes = 25)):
        return [weather, "SUNRISE"]#, current_in_utc, ["sunset", sunset_in_utc]]

    if sunset_in_utc >  current_in_utc and sunrise_in_utc < current_in_utc:
        return [weather, "DAYTIME"]#, current_in_utc, ["sunset", sunset_in_utc]]

    if sunset_in_utc <  current_in_utc or sunrise_in_utc > current_in_utc:
        return [weather, "NIGHTTIME"]#, current_in_utc, ["sunset", sunset_in_utc]]

    return []

def google_api(lat, lon):
    query_result = google_places.nearby_search(lat_lng={"lat":lat, "lng":lon}, radius=20)
    info = []
    ignore = [] #['route', 'locality', 'political']
    for place in query_result.places:
        if True not in [p in ignore for p in place.types]:
            info += [place.name] + place.types

    return info

#@app.route('/yelp', methods=['GET'])
def yelp_api(lat, lon):
    print("inside yelp!")
    tags = []
    affordances = []
    names = []

    params = {
    	"radius_filter" : 40,
    	"limit" : 3,
        "sort" : 1, #sort by distance
    	"open_now" : True,
    }
    resp = yelp_client.search_by_coordinates(lat, lon, **params)
    print(resp)
    info = []
    if not resp.businesses:
        return []
    for b in resp.businesses:
        name = b.name
        print(name)
        categories = [c[1] for c in b.categories]
        print(categories)
        info = info + categories + [name]
        print(info)
    return info

@app.route('/test_locations/<string:lat>/<string:lon>', methods=['GET'])
def test_yelp(lat, lon):
    print("inside yelp!")
    tags = []
    affordances = []
    names = []

    params = {
        "limit" : 10,
        "sort" : 1, #sort by distance
    }
    resp = yelp_client.search_by_coordinates(float(lat), float(lon), **params)
    print(resp)
    info = []
    if not resp.businesses:
        return []
    for b in resp.businesses:
        name = b.name
        print(name)
        categories = [c[1] for c in b.categories]
        print(categories)
        info = info + [[name]+categories]
        print(info)
    return jsonify(info)


@app.route("/")
def hello():
    return "Hello World!"


if __name__ == '__main__':
    app.run(debug=True, port=int(environ.get("PORT", 5000)), host='0.0.0.0')
