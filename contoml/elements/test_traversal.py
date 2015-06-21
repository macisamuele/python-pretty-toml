from contoml.elements.test_common import DummyFile


def test_traversal():
    dummy_file = DummyFile()

    assert dummy_file._find_following_opening_square_bracket(-1) == 1
    assert dummy_file._find_following_opening_square_bracket(1) == 20
    assert dummy_file._find_following_opening_square_bracket(20) < 0

    assert dummy_file._find_preceding_table(30) == 26
    assert dummy_file._find_preceding_table(26) == 18
    assert dummy_file._find_preceding_table(18) == 11
    assert dummy_file._find_preceding_table(11) == 5
    assert dummy_file._find_preceding_table(5) == 0
    assert dummy_file._find_preceding_table(0) < 0
