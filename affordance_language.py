from itertools import cycle
from random import shuffle
from pprint import pprint
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS

import yelp_academic_etl as etl


def natlang2keywords(aff):
    """
    Parameters
    ----------
    aff: str,
        i.e. Someone in a downtown riding their bike

    Returns
    -------
    keywords: list of str
        i.e. ['downtown', 'riding', 'bike']
    """
    return [w for w in aff.lower().strip().split(' ')
            if w not in ENGLISH_STOP_WORDS]


def test_natlang2keywords():
    assert (['downtown', 'riding', 'bike'] ==
            natlang2keywords("Someone in a downtown riding their bike"))
    assert (['downtown', 'riding', 'bike'] ==
            natlang2keywords("Someone in a downtown riding their bike\n"))


def preload_affordances(txtfile):
    with open(txtfile, "r") as f:
        affs = f.readlines()

    return affs


def main():

    print("Loading...")
    affs = preload_affordances("storytime_affordances.txt")
    # shuffle(affs)
    affs_generator = cycle(affs)
    X, cats, vocab = etl.load_tfidf("sklearn-with-stopwords")

    query = raw_input("Type a natural language affordance requirement:\n")
    while (query != 'q'):

        if query == '':
            query = next(affs_generator)

        keywords = natlang2keywords(query)
        obj1 = {}
        obj1["affordance.   "] = query
        obj1["keywords      "] = keywords
        pprint(obj1)

        cats_tfidf = etl.query_categories_by_many(keywords, X, cats, vocab)
        categories = list(cats_tfidf["feature"].get_values())
        obj2 = {}
        obj2["yelp category "] = categories
        pprint(obj2)

        query = raw_input("Type another affordance query:\n")

if __name__ == '__main__':
    main()
