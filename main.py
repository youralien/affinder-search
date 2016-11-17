from flask import Flask, jsonify
import pyrebase
import math
import json
import uuid
import requests
import datetime
from yelp.client import Client
from yelp.oauth1_authenticator import Oauth1Authenticator
from os import environ



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

app = Flask (__name__)

firebase = pyrebase.initialize_app(firebase_config)
db = firebase.database()

def calculateDistance(x1,y1,x2,y2):
     dist = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
     return dist



@app.route('/games/<string:lat>/<string:lon>', methods=['GET'])
def get_games(lat, lon):
	lat = float(lat)
	lon = float(lon)

	conditions = get_current_conditions(lat, lon)
	print(conditions)
	all_games = db.child("games").get()
	for g in all_games.each():
		game = dict(g.val())
		print(game)

		if(game["weather"] not in conditions["weather"]):
			print(g.key() + "weather false")
			continue
		if(game["affordances"] not in conditions["affordances"]):
			print(g.key() + "affordacnes false")
			continue
		if(not (game["start_time"] <= conditions["hours"])):
			print(g.key() + "too early")
			continue
		if(not (game["end_time"] >= conditions["hours"])):
			print(g.key() + "too late")
			continue	
		
		return jsonify(g.val())

	return "no games"


@app.route('/test', methods=['GET'])
def testing():
	return "PARTY PARROTS!!"


@app.route('/conditions/<string:lat>/<string:lon>', methods=['GET'])
def return_conditions(lat, lon):
	lat = float(lat)
	lon = float(lon)
	conditions = get_current_conditions(lat, lon)
	return jsonify(conditions)

def get_current_conditions(lat, lon):
	current_conditions = {"hours":0, "minutes":0, "affordances":[], "weather":"no info yet"}
	current_conditions["weather"] = get_weather(lat, lon)
	(names, tags, affordances) = get_affordances_from_location(lat, lon)
	(y_names, y_tags, y_affordances) = yelp_api(lat, lon)
	current_conditions["location_names"] = names + y_names
	current_conditions["location_tags"] = tags + y_tags
	current_conditions["affordances"] = affordances + y_affordances
	current_conditions["hours"] = datetime.datetime.now().hour
	current_conditions["minutes"] = datetime.datetime.now().minute

	key = uuid.uuid4().hex
	data = {key: current_conditions}
	db.child("current_conditions").set(data)
	return current_conditions

def get_affordances_from_location(clat, clon):
	locations = db.child("campus_locations").get()
	location_names = []
	location_tags = []
	nearby_affordances = []

	for loc in locations.each():
		loc_info = dict(loc.val())
		distance = math.sqrt((loc_info['lat']-clat)**2 + (loc_info['lon']-clon)**2)
		
		if (distance < .005):
			location_names.append(loc_info["name"])
			location_tags = get_location_tags(loc_info["name"])
			nearby_affordances = nearby_affordances + get_affordances(location_tags)

	return (location_names, location_tags, nearby_affordances)

def get_location_tags(location_name):
	return db.child("location_tags").child(location_name).get().val()

def get_affordances(location_tags):
	print("get affordacnes for ", location_tags, "\n \n \n \n")
	all_affordances = []
	for tag in location_tags:
		affordances = db.child("tag_affordances").child(tag).get()
		if affordances.val():
			all_affordances = all_affordances + affordances.val()
	print(all_affordances)	
	return all_affordances
	
def get_weather(curr_lat, curr_lon):
	url = "http://api.openweathermap.org/data/2.5/weather?lat=" + str(curr_lat) + "&lon=" + str(curr_lon) + "&appid=" + WEATHER_API_KEY
	response = (requests.get(url)).json()
	weather = ""
	for w in response["weather"]:
		weather = weather + w["description"] + " "

	return weather


#@app.route('/yelp', methods=['GET'])
def yelp_api(lat, lon):
	categories = ["coffee", "parks"]
	tags = []
	affordances = []
	names = []

	for c in categories:
		params = {
			"category_filter" : c,
			"radius_filter" : 100,
			"limit" : 1,
		}
		
		resp = yelp_client.search_by_coordinates(lat, lon, **params)
		print(resp)
		for b in resp.businesses:
			names.append(c)
			tags = tags + get_location_tags(c)
			affordances = affordances + get_affordances(tags)
			print(b.name, b.categories)
	
	return (names, tags, affordances)


def populate_test_db():
	data = {uuid.uuid4().hex: {"name": "Lakefill", "lat": 42, "lon": -87}, 
			uuid.uuid4().hex: {"name": "Tech", "lat":42.057798, "lon": -87.676246} }
	
	db.child("campus_locations").set(data)

	data1 = {"classroom": {0:"sit", 1:"write"},
			 "tree": {0: "hug", 1:"observe"},
			 "grassy_space" : {0: "lie", 1:"roll"}}
 	
	db.child("tag_affordances").set(data1)

	data2 = {"Tech": {0:"classroom"},
			 "Lakefill": {0: "tree", 1:"grassy_space"}}
 	
	db.child("location_tags").set(data2)



if __name__ == '__main__':
    app.run(debug=False, port=environ.get("PORT", 5000), host='0.0.0.0')


@app.route("/")
def hello():
	return "Hello World!"
