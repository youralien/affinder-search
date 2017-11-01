"""
search_yelp_places.py

Usage:

python search_yelp_places.py "someone who is walking their dog"

"""
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

    # TODO(rlouie): edit output to be handled by meteor command
    # See meteor calling python script example:
    # https://github.com/NUDelta/pair-research-meteor/blob/9536ec12d03f339d75fdc9d6dda8329dbf0cdc13/imports/api/pairings/methods.js#L94

    print search_yelp_places_that_afford(args.query)
