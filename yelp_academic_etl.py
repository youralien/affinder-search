import io
import os

import mysql.connector

import numpy as np

import pandas as pd

from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS, TfidfVectorizer

import spacy

import textacy


def cat2doc(cat):
    """Sushi Bars -> Sushi Bars.txt
    From Category to Document filepath """
    # Some categories have '/' in their name, which can throw off file paths.
    cat = cat.replace('/', '-')

    return "reviewtext/%s.txt" % cat


def cats2docs(categories):
    if isinstance(categories, str):
        categories = (categories, )

    return [cat2doc(cat) for cat in categories]


def all_categories():
    cnx = mysql.connector.connect(user='root', password='gottagofast',
                                  host='127.0.0.1',
                                  database='yelp_db')

    cursor = cnx.cursor()

    query = ("SELECT DISTINCT category.category FROM category")
    cursor.execute(query)

    categories = [category for category, in cursor]

    cursor.close()
    cnx.close()

    return categories


def write_document(cursor, cat):
    """ Given a yelp category, build out a text document
    which has all the reviews for that category """
    query = ("SELECT review.text "
             "FROM review INNER JOIN category "
             "ON review.business_id = category.business_id "
             "WHERE category.category=%s")
    cursor.execute(query, (cat,))

    n_encoding_errors = 0
    n_review = 0
    with io.open(cat2doc(cat), 'w', encoding='utf8') as f:
        for text, in cursor:
            try:
                f.write(text)
                f.write(unicode("\n"))
            except UnicodeEncodeError:
                n_encoding_errors += 1
            n_review += 1
    return n_encoding_errors, n_review


def sql2txt(categories, recompute=False):
    cnx = mysql.connector.connect(user='root', password='gottagofast',
                                  host='127.0.0.1',
                                  database='yelp_db')

    cursor = cnx.cursor()

    if isinstance(categories, str):
        categories = (categories, )

    for cat in categories:
        if recompute or not os.path.exists(cat2doc(cat)):
            n_errors, n_total = write_document(cursor, cat)
            print("%s: %d errors, %d total" % (cat, n_errors, n_total))

    cursor.close()
    cnx.close()


def create_all_documents():
    cats = all_categories()
    print("Creating %d documents" % len(cats))
    sql2txt(cats)


def document_text_iterator(categories):
    for filepath in cats2docs(categories):
        with io.open(filepath, 'r', encoding='utf8') as f:
            yield f.read()

def document_iterator(categories):
    for filepath in cats2docs(categories):
        yield filepath

def vectorize_sklearn(categories):
    # should I use the vocabulary from something like fasttext?
    vect = TfidfVectorizer(input='filename',
                           vocabulary=None, stop_words=ENGLISH_STOP_WORDS)
    X = vect.fit_transform(document_iterator(categories))
    vocabulary = vect.get_feature_names()
    return (X, categories, vocabulary)


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


def top_tfidf_feats(row, features, top_n=25):
    """ Get top n tfidf values in row and return them with their corresponding
    feature names.
    Source: https://buhrmann.github.io/tfidf-analysis.html
    """
    topn_ids = np.argsort(row)[::-1][:top_n]
    top_feats = [(features[i], row[i]) for i in topn_ids]
    df = pd.DataFrame(top_feats)
    df.columns = ['feature', 'tfidf']
    return df


def top_feats_in_doc(X, features, row_id, top_n=25):
    """ Top tfidf features in specific document (matrix row)
    Source: https://buhrmann.github.io/tfidf-analysis.html
    """
    row = np.squeeze(X[row_id].toarray())
    return top_tfidf_feats(row, features, top_n)

if __name__ == '__main__':
    # categories = ('Sushi Bars',
    #               'Bikes',
    #               'Dance Clubs')

    categories = all_categories()
    X, categories, vocabulary = vectorize_sklearn(categories)

    np.savez_compressed('tfidf/stopword-sklearn',
        X=X, categories=categories, vocabulary=vocabulary)
    # for i, cat in enumerate(categories):
    #     print cat
    #     print top_feats_in_doc(X, vocabulary, i)
