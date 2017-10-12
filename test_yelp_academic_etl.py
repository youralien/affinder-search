from yelp_academic_etl import (
    cat2doc,
    cats2docs,
    sql2txt,
    document_text_iterator,
    vectorize_sklearn
)


def test_cat2doc():
    assert "reviewtext/Naturopathic-Holistic.txt" == \
           cat2doc("Naturopathic/Holistic")
    assert "reviewtext/Japanese.txt" == cat2doc('Japanese')


def test_cats2docs():
    truths = ["reviewtext/Naturopathic-Holistic.txt",
              "reviewtext/Japanese.txt"]
    cats = ["Naturopathic/Holistic",
            "Japanese"]
    outs = cats2docs(cats)
    for truth, out in zip(truths, outs):
        assert truth == out


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

# test_vectorizer_sklearn()


# def test_vectorizer_textacy():
#     X, categories, vocabulary = vectorize_textacy('Japanese')
#     X, categories, vocabulary = vectorize_textacy(('Japanese', 'Korean'))

# test_vectorizer_textacy()
