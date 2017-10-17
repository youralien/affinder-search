import re
from itertools import cycle
# from random import shuffle
from pprint import pprint
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
from gensim.models import KeyedVectors

import yelp_academic_etl as etl


def create_constrained_language():
    lang = set(ENGLISH_STOP_WORDS)

    with open('constrained-language.txt', 'r') as f:
        lines = f.readlines()

    for line in lines:
        w = line.strip().lower()
        lang.add(w)

    return lang

CONSTRAINED_LANGUAGE = create_constrained_language()


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
    words = aff.strip().lower().split(' ')
    regex = re.compile('[^a-z]')
    keywords = []
    for w in words:
        w_stripped = regex.sub('', w)
        if w_stripped and w_stripped not in CONSTRAINED_LANGUAGE:
            keywords.append(w_stripped)
    return keywords


def preload_affordances(txtfile):
    with open(txtfile, "r") as f:
        affs = f.readlines()

    return affs


def main():

    top_n = 50
    print("Loading...")
    EMBEDDING = KeyedVectors.load_word2vec_format('wiki.en/wiki.en.vec',
                                                  limit=100000)
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

        # expand your keywords, and thus the categories
        dfs = []
        for kw in keywords:
            if kw not in CONSTRAINED_LANGUAGE:
                try:
                    similar_kws = map(lambda x: x[0],
                                      EMBEDDING.most_similar(kw)[:3])
                    similar_kws.append(kw)
                    print similar_kws

                    # by taking union of similar keywords
                    dfs.append(etl.query_categories_by_many(similar_kws,
                                                            X,
                                                            cats,
                                                            vocab,
                                                            'outer',
                                                            top_n))
                except KeyError:
                    # Word not in embedding vocab
                    dfs.append(etl.query_categories_by_word(kw, X, cats,
                                                            vocab, top_n))

        # take the intersection of all the words
        cats_tfidf = etl.merge_many_dfs(dfs, 'inner')
        # cats_tfidf = etl.query_categories_by_many(keywords, X, cats, vocab)
        categories = list(cats_tfidf["feature"].get_values())
        obj2 = {}
        obj2["yelp category "] = categories
        pprint(obj2)

        query = raw_input("Type another affordance query:\n")

if __name__ == '__main__':
    main()
