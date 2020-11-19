import json
import tqdm
from elasticsearch import Elasticsearch
from elasticsearch.helpers import streaming_bulk

# Note: This small version is ~15k lines/documents, while the full dataset is 8million
# Created the small dataset using the following command
# head -n 15000 yelp_academic_dataset_review.json > yelp_academic_dataset_review_small.json
REVIEW_JSON = '/Users/ryan/data/yelp_dataset/yelp_academic_dataset_review_small.json'

def create_index(client):
    """Creates an index in Elasticsearch if one isn't already there."""
    client.indices.create(
        index="yelp-reviews-small",
        body={
            "settings": {"number_of_shards": 1},
            "mappings": {
                "properties": {
                    "review_id": {"type": "keyword"},
                    "business_id": {"type": "keyword"},
                    "text": {"type": "text"}
                }
            },
        },
        ignore=400,
    )

def generate_actions():
    with open(REVIEW_JSON, 'r') as f:
        for line in iter(f.readline, ''):
            row = json.loads(line)
            doc = {
                "_id": row["review_id"],
                "business_id": row["business_id"],
                "text": row["text"]
            }
            yield doc 


def main():
    client = Elasticsearch() 

    number_of_docs = 15000

    print("Creating an index...")
    create_index(client)

    print("Indexing documents...")
    progress = tqdm.tqdm(unit="docs", total=number_of_docs)
    successes = 0
    for ok, action in streaming_bulk(
        client=client, index="yelp-reviews-small", actions=generate_actions(),
    ):
        progress.update(1)
        successes += ok
    print("Indexed %d/%d documents" % (successes, number_of_docs))
    

if __name__ == "__main__":
    print("Running main")
    main()
