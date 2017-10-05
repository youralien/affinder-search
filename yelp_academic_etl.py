import io

import mysql.connector

# from sklearn.feature_extraction.text


def write_document(cursor, cat):
    """ Given a yelp category, build out a text document
    which has all the reviews for that category """
    query = ("SELECT review.text "
             "FROM review INNER JOIN category ON review.business_id = category.business_id "
             "WHERE category.category=%s")
    cursor.execute(query, (cat,))

    n_encoding_errors = 0
    n_review = 0
    with io.open("reviewtext/%s.txt" % cat, 'w', encoding='utf8') as f:
        for text, in cursor:
            try:
                f.write(text)
                f.write(unicode("\n"))
            except UnicodeEncodeError, e:
                n_encoding_errors += 1
            n_review += 1
    return n_encoding_errors, n_review

def main():
    cnx = mysql.connector.connect(user='root', password='gottagofast',
                                  host='127.0.0.1',
                                  database='yelp_db')

    cursor = cnx.cursor()
    cat = "Sushi Bars"
    n_errors, n_total = write_document(cursor, cat)
    print("%s: %d errors, %d total" % (cat, n_errors, n_total))
    cursor.close()
    cnx.close()

if __name__ == '__main__':
    main()