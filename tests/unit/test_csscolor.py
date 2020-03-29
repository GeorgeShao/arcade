def test_csscolors(mock_window):
    from arcadeplus import csscolor
    names = csscolor.__dict__.keys()
    assert 156 == len(names)
