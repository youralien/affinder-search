# -*- coding: utf-8 -*-
# @Author: youralien
# @Date:   2018-02-20 02:05:38
# @Last Modified by:   youralien
# @Last Modified time: 2018-03-06 23:02:44

from flask import Flask, jsonify
from ordered_set import OrderedSet

from yelp_academic_etl import (
    load_tfidf, query_categories_by_many, query_categories_by_word)
from explore_embedding import query_expansion

app = Flask(__name__)

X, cats, vocab = load_tfidf("sklearn-with-stopwords")


@app.route("/categories/<string:query>/")
def retrieve_yelp_categories(query):
    query = query.replace('+', ' ')

    expanded_keywords = query_expansion(query)

    accum_cats = OrderedSet()
    for keywords in expanded_keywords:
        if len(keywords) == 1:
            cats_tfidf = query_categories_by_word(keywords[0], X, cats, vocab,
                                                  top_n=25)
        else:
            cats_tfidf = query_categories_by_many(keywords, X, cats, vocab,
                                                  top_n=25)

        categories = list(cats_tfidf["feature"].get_values())

        for cat in categories:
            accum_cats.add(cat)

    print(accum_cats)
    return jsonify(list(accum_cats))

if __name__ == '__main__':
    app.run(port=8000, host='localhost')
