from elasticsearch import Elasticsearch 
from flask import Flask, jsonify

client = Elasticsearch()

app = Flask(__name__)

@app.route("/search/<string:query>/")
def search(query):
    query = query.replace('+', ' ')
    resp = client.search(index='yelp-reviews-small', body={"query": {"match": {"text": query }}})
    return jsonify(resp)


if __name__ == '__main__':
    app.run(port=8080, host='localhost')
