# -*- coding: utf-8 -*-
# @Author: youralien
# @Date:   2018-02-20 04:33:50
# @Last Modified by:   youralien
# @Last Modified time: 2018-02-20 04:56:04

import spacy
import textacy

from yelp_academic_etl_training import (
    document_text_iterator)


def vectorize_textacy(categories):

    corpus = textacy.Corpus(spacy.load('en'),
                            texts=document_text_iterator(categories))
    terms_list = (doc.to_terms_list(ngrams=1, as_strings=True)
                  for doc in corpus)
    vect = textacy.Vectorizer(
        weighting='tfidf', normalize=True, smooth_idf=True,
        min_df=2, max_df=0.95)
    X = vect.fit_transform(terms_list)
    vocabulary = vect.feature_names

    return (X, categories, vocabulary)
