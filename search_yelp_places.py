"""
search_yelp_places.py

Usage:

python search_yelp_places.py "someone who is walking their dog"

"""
import json
from affordance_language import natlang2keywords
from yelp_academic_etl import load_tfidf, query_categories_by_many


def search_yelp_places_that_afford(query):
    """ This version does not use embeddings to expand the keywords
    Parameters
    ----------
    query: str, affordance query
    """
    X, cats, vocab = load_tfidf("sklearn-with-stopwords")
    keywords = natlang2keywords(query)

    cats_tfidf = query_categories_by_many(keywords, X, cats, vocab)
    categories = list(cats_tfidf["feature"].get_values())
    return categories


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description="Search Yelp for Place \
                categories matching Affordance Keywords")
    parser.add_argument('query', type=str, help='a simple, natural language \
        query')

    args = parser.parse_args()

    place_categories = search_yelp_places_that_afford(args.query)
    place_categories = [elem.encode('ascii', 'ignore')
                        for elem in place_categories]
    print(json.dumps(place_categories))
