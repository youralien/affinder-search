# -*- coding: utf-8 -*-
# @Author: youralien
# @Date:   2018-02-20 02:05:38
# @Last Modified by:   youralien
# @Last Modified time: 2018-03-10 11:14:36

from flask import Flask, jsonify

from yelp_academic_etl import (
    load_tfidf, query_categories_by_many, query_categories_by_word,
    merge_many_dfs)
from explore_embedding import query_expansion

app = Flask(__name__)

X, cats, vocab = load_tfidf("sklearn-with-stopwords")


@app.route("/categories/<string:query>/")
def retrieve_yelp_categories(query):
    query = query.replace('+', ' ')

    expanded_keywords = query_expansion(query)

    # accum_cats = OrderedSet()
    dfs = []
    for keywords, cossim in expanded_keywords:
        print("keywords:\n", keywords)
        if len(keywords) == 1:
            cats_tfidf = query_categories_by_word(keywords[0], X, cats, vocab,
                                                  top_n=25)
        else:
            cats_tfidf = query_categories_by_many(keywords, X, cats, vocab,
                                                  top_n=25)

        dfs.append(cats_tfidf)

    if (len(dfs) > 1):
        combo_df = merge_many_dfs(dfs, 'outer')
        top_n_df = combo_df[:25]
        categories = list(top_n_df["feature"].get_values())
    else:
        categories = list(cats_tfidf["feature"].get_values())
    print(categories)
    return jsonify(list(categories))

if __name__ == '__main__':
    app.run(port=8000, host='localhost')
