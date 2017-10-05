import io

import mysql.connector

from sklearn.feature_extraction.text import TfidfVectorizer

def cat2doc(cat):
    """ Sushi Bars -> Sushi Bars.txt 
    From Category to Document filepath """
    return "reviewtext/%s.txt" % cat

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

def sql2txt(categories):
    cnx = mysql.connector.connect(user='root', password='gottagofast',
                                  host='127.0.0.1',
                                  database='yelp_db')

    cursor = cnx.cursor()

    if isinstance(categories, str):
        categories = (categories, )

    for cat in categories:
        n_errors, n_total = write_document(cursor, cat)
        print("%s: %d errors, %d total" % (cat, n_errors, n_total))

    cursor.close()
    cnx.close()

def vectorize(categories):
    if isinstance(categories, str):
        categories = (categories, )

    categories = [cat2doc(cat) for cat in categories]

    # should I use the vocabulary from something like fasttext?
    # stop words: sklearn.feature_extraction.text.ENGLISH_STOP_WORDS
    vect = TfidfVectorizer(input='filename', vocabulary=None, stop_words=None)

    X = vect.fit_transform(categories)
    return (X, vect)



if __name__ == '__main__':
    X, vect = vectorize(('Sushi Bars', 'Korean', 'Japanese'))
