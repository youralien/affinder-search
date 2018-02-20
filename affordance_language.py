import os
import re
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS


def create_constrained_language():
    lang = set(ENGLISH_STOP_WORDS)

    with open(os.path.join(os.path.dirname(__file__),
              'constrained-language.txt'), 'r') as f:
        lines = f.readlines()

    for line in lines:
        w = line.strip().lower()
        lang.add(w)

    return lang

CONSTRAINED_LANGUAGE = create_constrained_language()


def natlang2keywords(aff):
    """
    Parameters
    ----------
    aff: str,
        i.e. Someone in a downtown riding their bike

    Returns
    -------
    keywords: list of str
        i.e. ['downtown', 'riding', 'bike']
    """

    words = aff.strip().lower().split(' ')
    regex = re.compile('[^a-z]')
    keywords = []
    for w in words:
        w_stripped = regex.sub('', w)
        if w_stripped and w_stripped not in CONSTRAINED_LANGUAGE:
            keywords.append(w_stripped)
    return keywords


def preload_affordances(txtfile):
    with open(txtfile, "r") as f:
        affs = f.readlines()

    return affs
