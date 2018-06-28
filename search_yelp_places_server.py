# -*- coding: utf-8 -*-
# @Author: youralien
# @Date:   2018-02-20 02:05:38
# @Last Modified by:   youralien
# @Last Modified time: 2018-06-28 14:45:31

from flask import Flask, jsonify

from affordance_language import natlang2keywords
from yelp_academic_etl import (
    load_tfidf, query_categories_by_many, query_categories_by_word,
    category_title2alias)

app = Flask(__name__)

X, cats, vocab = load_tfidf("sklearn-with-stopwords")
cats = category_title2alias(cats)


@app.route("/categories/<string:query>/")
def retrieve_yelp_categories(query):
    query = query.replace('+', ' ')
    keywords = natlang2keywords(query)
    if len(keywords) == 1:
        cats_tfidf = query_categories_by_word(keywords[0], X, cats, vocab,
                                              top_n=25)
    else:
        cats_tfidf = query_categories_by_many(keywords, X, cats, vocab,
                                              top_n=25)

    categories = set(cats_tfidf["feature"].get_values())
    categories.remove('')   # depreciated
    categories = list(categories)
    return jsonify(categories)


if __name__ == '__main__':
    app.run(port=8000, host='localhost')
