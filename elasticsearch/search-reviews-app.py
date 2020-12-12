from elasticsearch import Elasticsearch 
from flask import Flask, jsonify

client = Elasticsearch()

app = Flask(__name__)

@app.route("/search/<string:query>/")
def search(query):
    query = query.replace('+', ' ')
    resp = client.search(index='yelp-reviews-small', body={"query": {"match": {"text": query }}})
    return jsonify(resp)

@app.route("/cleansearch/<string:query>/")
def cleansearch(query):
    query = query.replace('+', ' ')
    resp = client.search(index='yelp-reviews-small', body={"query": {"match": {"text": query }}})
    
    # text is in resp[hits][hits][i][_source][text]
    # score is in resp[hits][hits][i][_score]

    texts = []
    for hit in resp["hits"]["hits"]:
        text = hit["_source"]["text"]  
        score = hit["_score"]
        texts.append(text)

    return jsonify(texts)

if __name__ == '__main__':
    app.run(port=8080, host='localhost')
