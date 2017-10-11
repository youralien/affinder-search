from yelp_academic_etl import *


def test_cat2doc():
    assert "reviewtext/Naturopathic-Holistic.txt" == cat2doc("Naturopathic/Holistic")
    assert "reviewtext/Japanese.txt" == cat2doc('Japanese')

test_cat2doc()


def test_cats2docs():
    truths = ["reviewtext/Naturopathic-Holistic.txt",
              "reviewtext/Japanese.txt"]
    cats = ["Naturopathic/Holistic",
            "Japanese"]
    outs = cats2docs(cats)
    for truth, out in zip(truths, outs):
        assert truth == out

test_cats2docs()


def test_sql2txt():
    sql2txt('Japanese')
    sql2txt(('Japanese', 'Korean'))
    sql2txt('Japanese', recompute=True)
    sql2txt(('Japanese', 'Korean'), recompute=True)

test_sql2txt()


def test_document_text_iterator():
    docs = ('Japanese', 'Korean')
    for doc in document_text_iterator(docs):
        print doc[:100]

test_document_text_iterator()


def test_vectorizer_sklearn():
    X, categories, vocabulary = vectorize_sklearn('Japanese')
    X, categories, vocabulary = vectorize_sklearn(('Japanese', 'Korean'))

# test_vectorizer_sklearn()


def test_vectorizer_textacy():
    X, categories, vocabulary = vectorize_textacy('Japanese')
    X, categories, vocabulary = vectorize_textacy(('Japanese', 'Korean'))

# test_vectorizer_textacy()
