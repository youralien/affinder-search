from affordance_language import natlang2keywords


def test_natlang2keywords():
    assert (['downtown', 'riding', 'bike'] ==
            natlang2keywords("Someone in a downtown riding their bike"))
    assert (['downtown', 'riding', 'bike'] ==
            natlang2keywords("Someone in a downtown riding their bike\n"))
    assert (['cat', 'box'] ==
            natlang2keywords("cat, box\n"))
    assert (['cat', 'dog'] ==
            natlang2keywords("person with a cat and dog\n"))
