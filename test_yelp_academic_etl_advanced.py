# -*- coding: utf-8 -*-
# @Author: youralien
# @Date:   2018-02-20 04:34:26
# @Last Modified by:   youralien
# @Last Modified time: 2018-02-20 04:37:39

from yelp_academic_etl_advanced import vectorize_textacy


def test_vectorizer_textacy():
    X, categories, vocabulary = vectorize_textacy('Japanese')
    X, categories, vocabulary = vectorize_textacy(('Japanese', 'Korean'))
