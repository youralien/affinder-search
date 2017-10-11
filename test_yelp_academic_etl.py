from yelp_academic_etl import *

def test_cat2doc():
	assert "reviewtext/Naturopathic-Holistic.txt" == cat2doc("Naturopathic/Holistic")
	assert "reviewtext/Japanese.txt" == cat2doc('Japanese')

test_cat2doc()

def test_sql2txt():
	sql2txt('Japanese')
	sql2txt(('Japanese', 'Korean'))
	sql2txt('Japanese', recompute=True)
	sql2txt(('Japanese', 'Korean'), recompute=True)


test_sql2txt()
