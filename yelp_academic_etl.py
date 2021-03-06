import os
import json
import pickle
import numpy as np
import pandas as pd


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
    col = X[:, col_id].toarray()
    col = np.squeeze(col)
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


def load_pickle(filename):
    with open(filename, 'rb') as infile:
        try:
            matrix = pickle.load(infile)
        except UnicodeDecodeError:
            # Python 2 object to Python 3
            infile.seek(0)
            matrix = pickle.load(infile, encoding="latin-1")
    return matrix


def load_tfidf(fileprefix):
    X = load_pickle(os.path.join(os.path.dirname(__file__),
                    'tfidf/%s-X.mtx' % fileprefix))
    meta = np.load(os.path.join(os.path.dirname(__file__),
                   'tfidf/%s-meta.npz' % fileprefix))

    return X, meta['categories'], meta['vocabulary']


def title2alias_dict(v3file='categories.json'):
    """ Converts v2 titles to v3 aliases.
    For example, kv["Shopping"] = 'shopping'

    Parameters
    ----------
    v3file: path to v3 file
    category_titles: list of category titles
    """
    v3_cats_json = json.load(open(v3file, 'r'))
    kv = {cat['title']: cat['alias'] for cat in v3_cats_json}

    # handcoded translation from v2 titles to v3 aliases
    # FIXME: some of the aliases
    depreciated_titles_aliases = {
        '& Probates': 'willstrustsprobates',
        'Beer': 'beer_and_wine',
        'Books': 'media',
        'Ethic Grocery': 'ethicgrocery',
        'Mags': 'media',
        'Music & Video': 'media',
        'Pet Boarding/Pet Sitting': 'pet_sitting',  # petboarding too
        'Psychics & Astrologers': 'astrologers',    # psychics too
        'Trusts': 'willstrustsprobates',
        'Used': 'vintage',
        'Vintage & Consignment': 'vintage',
        'Vinyl Siding': 'vinylsiding',
        'Wills': 'willstrustsprobates',
        'Wine & Spirits': 'beer_and_wine',
        'Dry Cleaning & Laundry': 'laundromat',     # dryclean too
    }

    kv.update(depreciated_titles_aliases)

    return kv


def category_title2alias(categories):
    """
    Parameters
    ----------
    categories: list of strings
        yelp category titles

    Returns
    -------
    aliases: list of strings
        yelp category aliases
    """

    title2alias = title2alias_dict()
    aliases = []
    for cat_title in categories:
        try:
            aliases.append(title2alias[cat_title])
        except KeyError:
            aliases.append('')
    return aliases
