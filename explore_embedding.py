"""
Run from an ipython notebook to explore embeddings
"""

from gensim.models import KeyedVectors


EMB = KeyedVectors.load_word2vec_format('wiki.en/wiki.en.vec',
                                        limit=100000)

print("""
while True:
    print(map(lambda x: x[0], EMB.most_similar(raw_input("kw: "))))
""")

while True:
    print(map(lambda x: x[0], EMB.most_similar(raw_input("kw: "))))
