"""
Run from an ipython notebook to explore embeddings
"""

import numpy as np
from itertools import product
from gensim.models import KeyedVectors

from scipy.spatial.distance import cdist

from affordance_language import natlang2keywords
from yelp_academic_etl import load_tfidf

EMB = KeyedVectors.load_word2vec_format('wiki.en/wiki.en.vec',
                                        limit=100000)


X, cats, vocab = load_tfidf("sklearn-with-stopwords")
N_CATS = len(cats)


def single_word_expansion():
    print(map(lambda x: x[0], EMB.most_similar(raw_input("kw: "))))


def sentence_embedding(keywords):
    try:
        weights = map(lambda word: 1, keywords)
        weights = np.array(weights)
        # weights /= np.linalg.norm(weights, 2)
        # print("weights: ", weights)

        vectors = map(lambda word: EMB.get_vector(word), keywords)
        vectors = np.vstack(vectors)
        # print("vectors: ", vectors.shape)

        weighted_sum = np.dot(weights, vectors)
        # print("weighted_sum: ", weighted_sum.shape)

        # print("sim(p,x): ")
        # print(map(lambda tup: tup, EMB.similar_by_vector(weighted_sum)))
        return weighted_sum
    except KeyError:
        return np.zeros(300)


def query_expansion(query):
    keywords = natlang2keywords(query)
    q_emb = sentence_embedding(keywords)
    # TODO(rlouie): which tfidf weights do you use?  average of all?
    # and then do we normalize these so that the weights add to 1
    # weights = map(lambda word: query_categories_by_word(word, X, cats, vocab,
    #               N_CATS)['tfidf'].mean(), keywords)

    expansions = []
    for kw in keywords:
        similar_kws = map(lambda x: x[0],
                          EMB.most_similar(kw)[:3])
        similar_kws.append(kw)
        expansions.append(similar_kws)

    kw_phrases = [e for e in product(*expansions)]
    phrase_embeddings = np.vstack(
        [sentence_embedding(e) for e in product(*expansions)])

    distances = cdist(phrase_embeddings, q_emb.reshape(1, -1), 'cosine').flatten()
    idxs = np.argsort(distances)
    idxs = idxs[:int(1.5 * np.log2(len(idxs)))]
    final_kws = [(kw_phrases[idx], 1-distances[idx]) for idx in idxs]
    print("final_kws:\n", final_kws)
    # for kw, dist in final_kws:
    #     print(" ".join(e))

    return final_kws

if __name__ == '__main__':
    while True:
        query_expansion(raw_input("query: "))
