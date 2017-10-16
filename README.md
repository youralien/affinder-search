# Affordance Aware API

### Data for TF-IDF of Yelp Categories

You can find the TF-IDF matrix and the corresponding metadata [via this Dropbox link](https://www.dropbox.com/sh/hn4t4k9zbppm6dd/AAArh08p3n6C0YQAfsDGqVxda?dl=0).  You'll create a folder called `tfidf` at the top-level directory of this repository, and then download those files into there.

### Get affordances by location
Make a GET request to the following URL:
```
https://affordanceaware.herokuapp.com/conditions/<latitude>/<longitude>
```

pip freeze > requirements.txt

pip install -r requirements.txt

create .evn file


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
* gyms
* resturants

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
