"""
Run from an ipython notebook to explore embeddings
"""

import numpy as np
from gensim.models import KeyedVectors

from affordance_language import natlang2keywords
from yelp_academic_etl import (
    load_tfidf, query_categories_by_many, query_categories_by_word)

EMB = KeyedVectors.load_word2vec_format('wiki.en/wiki.en.vec',
                                        limit=100000)


X, cats, vocab = load_tfidf("sklearn-with-stopwords")
N_CATS = len(cats)


def single_word_expansion():
    print(map(lambda x: x[0], EMB.most_similar(raw_input("kw: "))))


def phrase_expansion():
    query = raw_input("query: ")
    keywords = natlang2keywords(query)

    # TODO(rlouie): which tfidf weights do you use?  average of all?
    # and then do we normalize these so that the weights add to 1
    weights = map(lambda word: query_categories_by_word(word, X, cats, vocab,
                  N_CATS)['tfidf'].mean(), keywords)
    weights = np.array(weights)
    print("weights: ", weights)

    vectors = map(lambda word: EMB.get_vector(word), keywords)
    vectors = np.vstack(vectors)
    print("vectors: ", vectors.shape)

    weighted_sum = np.dot(weights, vectors)
    print("weighted_sum: ", weighted_sum.shape)

    print("sim(p,x): ")
    print(map(lambda tup: tup[0], EMB.similar_by_vector(weighted_sum)))



if __name__ == '__main__':
    # pass
    while True:
        phrase_expansion()
