from scipy.sparse import random

from yelp_academic_etl import (
    cat2doc,
    cats2docs,
    sql2txt,
    document_text_iterator,
    vectorize_sklearn,
    all_categories,
    save_pickle,
    load_pickle,
    load_tfidf,
    query_categories_by_word,
    query_categories_by_many,
)


def test_cat2doc():
    docs = [
        "reviewtext/Naturopathic-Holistic.txt",
        "reviewtext/Japanese.txt"
    ]
    cats = [
        "Naturopathic/Holistic",
        "Japanese"
    ]

    for doc, cat in zip(docs, cats):
        assert doc == cat2doc(cat)

    outs = cats2docs(cats)
    for doc, out in zip(docs, outs):
        assert doc == out


def test_sql2txt():
    sql2txt('Japanese')
    sql2txt(('Japanese', 'Korean'))
    sql2txt('Japanese', recompute=True)
    sql2txt(('Japanese', 'Korean'), recompute=True)


def test_document_text_iterator():
    docs = ('Japanese', 'Korean')
    for doc in document_text_iterator(docs):
        print doc[:100]


def test_vectorizer_sklearn():
    X, categories, vocabulary = vectorize_sklearn('Japanese')
    X, categories, vocabulary = vectorize_sklearn(('Japanese', 'Korean'))


def test_all_categories():
    categories = all_categories()
    assert 1 == categories.count('Japanese')
    assert 1 == categories.count('Candle Stores')
    assert 1240 == len(categories)


def test_pickling():
    matrix = random(10000, 1000, density=0.001, format='csr')

    save_pickle(matrix, '/tmp/matrix.mtx')
    matrix_load = load_pickle('/tmp/matrix.mtx')

    assert matrix.shape == matrix_load.shape


def test_query_categories():
    X, cats, vocab = load_tfidf("sklearn-with-stopwords")

    query_categories_by_word("jumping", X, cats, vocab)
    query_categories_by_many(("jumping", "beautiful"), X, cats, vocab)
    query_categories_by_many(("jumping", "beautiful", "sun"), X, cats, vocab)
    query_categories_by_many(("jumping", "beautiful"), X, cats, vocab, 'outer')
    query_categories_by_many(("jumping", "beautiful", "sun"), X, cats, vocab,
                             'outer')


# def test_vectorizer_textacy():
#     X, categories, vocabulary = vectorize_textacy('Japanese')
#     X, categories, vocabulary = vectorize_textacy(('Japanese', 'Korean'))
