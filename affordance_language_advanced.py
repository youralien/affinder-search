# -*- coding: utf-8 -*-
# @Author: youralien
# @Date:   2018-02-20 05:01:10
# @Last Modified by:   youralien
# @Last Modified time: 2018-03-06 15:19:24

from gensim.models import KeyedVectors
from itertools import cycle
from random import shuffle
from pprint import pprint

from affordance_language import (
    natlang2keywords,
    preload_affordances,
    CONSTRAINED_LANGUAGE)
import yelp_academic_etl as etl


def yelp_places():

    top_n = 50
    print("Loading...")
    EMBEDDING = KeyedVectors.load_word2vec_format('wiki.en/wiki.en.vec',
                                                  limit=500000)
    affs = preload_affordances("storytime_affordances.txt")
    shuffle(affs)
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


def builtin_legos():

    print("Loading...")
    from lego_word_associations import lego_words

    EMBEDDING = KeyedVectors.load_word2vec_format('wiki.en/wiki.en.vec',
                                                  limit=100000)
    affs = preload_affordances("storytime_affordances.txt")
    shuffle(affs)
    affs_generator = cycle(affs)

    query = raw_input("Type a natural language affordance requirement:\n")
    while (query != 'q'):

        if query == '':
            query = next(affs_generator)

        keywords = set(natlang2keywords(query))
        obj1 = {}
        obj1["affordance.   "] = query
        obj1["keywords      "] = keywords
        pprint(obj1)

        expand_keywords = True
        if expand_keywords:
            for og_kw in keywords.copy():
                first_degree_kws = map(lambda tup: tup[0],
                                       EMBEDDING.most_similar(og_kw))

                for fd_kw in first_degree_kws:
                    keywords.add(fd_kw)
                    second_degree_kws = map(lambda tup: tup[0],
                                            EMBEDDING.most_similar(fd_kw))
                    for sd_kw in second_degree_kws:
                        keywords.add(sd_kw)

        obj2 = {}
        obj2["expanded words"] = keywords

        legos = set()
        for kw in keywords:
            for lego, word_assoc in lego_words.iteritems():
                if kw in word_assoc:
                    legos.add(lego)

        obj2["legos         "] = legos
        pprint(obj2)

        query = raw_input("Type another affordance query:\n")


def builtin_legos_syn():

    print("Loading...")
    from lego_word_associations import lego_words
    from oxford import synonyms

    # EMBEDDING = KeyedVectors.load_word2vec_format('wiki.en/wiki.en.vec',
    #                                               limit=100000)
    affs = preload_affordances("storytime_affordances.txt")
    shuffle(affs)
    affs_generator = cycle(affs)

    query = raw_input("Type a natural language affordance requirement:\n")
    while (query != 'q'):

        if query == '':
            query = next(affs_generator)

        keywords = set(natlang2keywords(query))
        obj1 = {}
        obj1["affordance.   "] = query
        obj1["keywords      "] = keywords
        pprint(obj1)

        expand_keywords = True
        if expand_keywords:
            for og_kw in keywords.copy():
                first_degree_kws = synonyms(og_kw)

                for fd_kw in first_degree_kws:
                    keywords.add(fd_kw)

        obj2 = {}
        obj2["expanded words"] = keywords

        legos = set()
        for kw in keywords:
            for lego, word_assoc in lego_words.iteritems():
                if kw in word_assoc:
                    legos.add(lego)

        obj2["legos         "] = legos
        pprint(obj2)

        query = raw_input("Type another affordance query:\n")


def builtin_legos_syn_emb():

    print("Loading...")
    from lego_word_associations import lego_words
    from oxford import synonyms

    EMBEDDING = KeyedVectors.load_word2vec_format('wiki.en/wiki.en.vec',
                                                  limit=100000)
    affs = preload_affordances("storytime_affordances.txt")
    shuffle(affs)
    affs_generator = cycle(affs)

    query = raw_input("Type a natural language affordance requirement:\n")
    while (query != 'q'):

        if query == '':
            query = next(affs_generator)

        keywords = set(natlang2keywords(query))
        obj1 = {}
        obj1["affordance.   "] = query
        obj1["keywords      "] = keywords
        pprint(obj1)

        expanded_keywords = set()
        for og_kw in keywords:
            first_degree_kws = synonyms(og_kw)

            for fd_kw in first_degree_kws:
                expanded_keywords.add(fd_kw)

        obj2 = {}
        obj2["expanded words"] = expanded_keywords

        refined_keywords = set()
        for candidate in expanded_keywords:
            use = True
            for word in keywords:
                try:
                    if (EMBEDDING.similarity(candidate, word) < 0.25):
                        use = False
                except KeyError:  # word not in vocab
                    use = False
            if use:
                refined_keywords.add(candidate)

        obj2["refined words"] = refined_keywords
        legos = set()
        for kw in refined_keywords:
            for lego, word_assoc in lego_words.iteritems():
                if kw in word_assoc:
                    legos.add(lego)

        obj2["z: legos         "] = legos
        pprint(obj2)

        query = raw_input("Type another affordance query:\n")

if __name__ == '__main__':
    yelp_places()