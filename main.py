from flask import Flask, jsonify
import pyrebase
import math
import json
import uuid
import requests
import datetime
from configparser import ConfigParser

def calculateDistance(x1,y1,x2,y2):
     dist = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
     return dist

config = ConfigParser()
config.read("secrets/config.ini")

WEATHER_API_KEY = config.get("weather", "api_key")
firebase_config = {
  "apiKey": config.get("firebase", "db_api_key"),
  "authDomain": config.get("firebase", "project_name")+".firebaseapp.com",
  "databaseURL": "https://"+config.get("firebase", "project_name")+".firebaseio.com",
  "storageBucket": config.get("firebase", "project_name") + ".appspot.com"
}

app = Flask (__name__)

firebase = pyrebase.initialize_app(firebase_config)
db = firebase.database()


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
	print(token)
	return jsonify(token)


@app.route('/conditions/<string:lat>/<string:lon>', methods=['GET'])
def return_conditions(lat, lon):
	lat = float(lat)
	lon = float(lon)
	conditions = get_current_conditions(lat, lon)
	return jsonify(conditions)

def get_current_conditions(lat, lon):
	current_conditions = {"hours":0, "minutes":0, "affordances":[], "weather":"no info yet"}
	current_conditions["weather"] = get_weather(lat, lon)
	current_conditions["affordances"] = get_campus_locations(lat, lon)
	current_conditions["hours"] = datetime.datetime.now().hour
	current_conditions["minutes"] = datetime.datetime.now().minute

	key = uuid.uuid4().hex
	data = {key: current_conditions}
	db.child("current_conditions").set(data)
	return current_conditions

def get_campus_locations(clat, clon):
	locations = db.child("campus_locations").get()
	location_names = []
	nearby_affordances = []

	for loc in locations.each():
		loc_info = dict(loc.val())
		distance = math.sqrt((loc_info['lat']-clat)**2 + (loc_info['lon']-clon)**2)
		
		if (distance < 10):
			location_tags = db.child("location_tags").child(loc_info["name"]).get()
			nearby_affordances = nearby_affordances + get_affordances(location_tags.val())

	return nearby_affordances

def get_affordances(location_tags):
	all_affordances = []
	for tag in location_tags:
		affordances = db.child("tag_affordances").child(tag).get()
		all_affordances = all_affordances + affordances.val()
		
	return all_affordances
	
def get_weather(curr_lat, curr_lon):
	url = "http://api.openweathermap.org/data/2.5/weather?lat=" + str(curr_lat) + "&lon=" + str(curr_lon) + "&appid=" + WEATHER_API_KEY
	response = (requests.get(url)).json()
	weather = ""
	for w in response["weather"]:
		weather = weather + w["description"] + " "

	return weather

def yelp_api():
	category = coffeeshops
	radius = 200;
	url = "https://api.yelp.com/v2/search?category_filter=" + category + "&radius_filter=" + radius + "&ll=" + lat + "," + lon

	37.788022,-122.399797


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
    app.run(debug=True)


@app.route("/")
def hello():
	return "Hello World!"
