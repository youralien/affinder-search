To run the microservice, run `python search-reviews-app.py`.
You can point queries to `localhost:8080/cleansearch/<query>`. It will return (max of 10) snippets of reviews that are most relevant to your query. See flask API for more details.

To expand the set of reviews, or the features available in the data, you'll have to ingest a different dataset than just the raw yelp reviews json.  
I haven't tried this, but I would expect you'd have to put the reviews JSON and business JSON into two collections into MongoDB; then denormalize for each review by linking the business with the review. Possibly parsing only the features you care about (e.g., business name, place category features). 
