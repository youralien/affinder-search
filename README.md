# Affordance Aware API
### Get affordances by location
Make a GET request to the following URL:
```
https://affordanceaware.herokuapp.com/conditions/<latitude>/<longitude>
```

The request will return a JSON with the following fields:
* affordances -- array of affordance
* daylight -- either true, false or SUNSET
* hours -- hour of current time
* location_names -- array of names of nearby locations
* location_tags -- array of objects at nearby locations
* minutes -- minutes of current time
* weather -- descption of current weather, see range of options [here](https://openweathermap.org/weather-conditions)

Supported location types include:
* Northwestern classrooms
* Northwestern student housing
* coffee shops
* parks

Example query while at a coffee shop in the evening:
```sh
$ curl -i http://0.0.0.0:5000/conditions/42.0582565/-87.6841178
```
```
{
  "affordances": [
    "eat", 
    "people_watch", 
    "sit"
  ], 
  "daylight": false, 
  "hours": 17, 
  "location_names": [
    "coffee"
  ], 
  "location_tags": [
    "food", 
    "people", 
    "table"
  ], 
  "minutes": 6, 
  "weather": "clear sky "
}

```
