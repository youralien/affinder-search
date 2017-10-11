import io
import os

import numpy as np
import pandas as pd
import mysql.connector
from sklearn.feature_extraction.text import TfidfVectorizer

def cat2doc(cat):
    """ Sushi Bars -> Sushi Bars.txt 
    From Category to Document filepath """

    # Some categories have '/' in their name, which can throw off file paths.
    cat = cat.replace('/', '-')

    return "reviewtext/%s.txt" % cat

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
             "FROM review INNER JOIN category ON review.business_id = category.business_id "
             "WHERE category.category=%s")
    cursor.execute(query, (cat,))

    n_encoding_errors = 0
    n_review = 0
    with io.open(cat2doc(cat), 'w', encoding='utf8') as f:
        for text, in cursor:
            try:
                f.write(text)
                f.write(unicode("\n"))
            except UnicodeEncodeError, e:
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

def vectorize(categories):
    if isinstance(categories, str):
        categories = (categories, )

    categories = [cat2doc(cat) for cat in categories]

    # should I use the vocabulary from something like fasttext?
    # stop words: sklearn.feature_extraction.text.ENGLISH_STOP_WORDS
    vect = TfidfVectorizer(input='filename', vocabulary=None, stop_words=None)

    X = vect.fit_transform(categories)
    vocabulary = vect.get_feature_names()

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
    X, categories, vocabulary = vectorize(('Sushi Bars', 'Bikes', 'Dance Clubs'))
    df = top_feats_in_doc(X, vocabulary, 0)

