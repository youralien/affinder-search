import io
import os
import cPickle as pickle
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


def top_tfidf_feats(array, features, top_n=25):
    """ Get top n tfidf values in array and return them with their corresponding
    feature names.
    Source: https://buhrmann.github.io/tfidf-analysis.html
    """
    topn_ids = np.argsort(array)[::-1][:top_n]
    top_feats = [(features[i], array[i]) for i in topn_ids]
    df = pd.DataFrame(top_feats)
    df.columns = ['feature', 'tfidf']
    return df


def top_feats_in_doc(X, features, row_id, top_n=25):
    """ Top tfidf features in specific document (matrix row)
    Source: https://buhrmann.github.io/tfidf-analysis.html
    """
    row = np.squeeze(X[row_id].toarray())
    return top_tfidf_feats(row, features, top_n)


def top_docs_for_word(X, document_names, col_id, top_n=25):
    """ Top docs by tfidf value for specific word (matrix col)
    """
    col = np.squeeze(X[:, col_id].toarray())
    return top_tfidf_feats(col, document_names, top_n)


def query_categories_by_word(word, X, categories, vocabulary, top_n=25):
    if isinstance(vocabulary, list):
        col_id = vocabulary.index(word)
    elif isinstance(vocabulary, np.ndarray):
        (col_id,), = np.where(vocabulary == word)

    return top_docs_for_word(X, categories, col_id, top_n)


def query_categories_by_many(words, X, categories, vocabulary, how='inner',
                             top_n=25):
    """ using syntax...
    df1.merge(df2,on='name').merge(df3,on='name')
    """
    dfs = []
    for word in words:
        try:
            # we use 4 * top_n because the intersection of 100 (default) top
            # categories for many words is a set that is likely to be small
            df = query_categories_by_word(word, X, categories, vocabulary,
                                          4 * top_n)
            dfs.append(df)
        except ValueError:
            print("Ignoring ", word)
            continue
    combo_df = merge_many_dfs(dfs, how)
    combo_df["tfidf"] = combo_df.sum(axis=1)
    combo_df = combo_df.sort_values("tfidf", ascending=False)
    return combo_df[:top_n]


def merge_many_dfs(dfs, how):
    chained_merge_cmd = (
        "dfs[%d].merge(dfs[%d],how='%s',on='feature')" % (0, 1, how))
    for i in range(2, len(dfs)):
        chained_merge_cmd += ".merge(dfs[%d],how='%s',on='feature')" % (i, how)

    return eval(chained_merge_cmd)


def save_pickle(matrix, filename):
    with open(filename, 'wb') as outfile:
        pickle.dump(matrix, outfile, pickle.HIGHEST_PROTOCOL)


def load_pickle(filename):
    with open(filename, 'rb') as infile:
        matrix = pickle.load(infile)
    return matrix


def load_tfidf(fileprefix):
    X = load_pickle(os.path.join(os.path.dirname(__file__),
                    'tfidf/%s-X.mtx' % fileprefix))
    meta = np.load(os.path.join(os.path.dirname(__file__),
                   'tfidf/%s-meta.npz' % fileprefix))
    return X, meta['categories'], meta['vocabulary']


if __name__ == '__main__':
    # categories = ('Sushi Bars',
    #               'Bikes',
    #               'Dance Clubs')

    categories = all_categories()
    X, categories, vocabulary = vectorize_sklearn(categories)

    save_pickle(X, 'tfidf/sklearn-with-stopwords-X.mtx')
    np.savez_compressed('tfidf/sklearn-with-stopwords-meta',
                        categories=categories, vocabulary=vocabulary)

    # for i, cat in enumerate(categories):
    #     print cat
    #     print top_feats_in_doc(X, vocabulary, i)
