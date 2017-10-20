from common.helper import f_repr, p_repr


def test_f_repr():
    assert f_repr(12.1234, 0) == '12'
    assert f_repr(12.1234, 1) == '12'
    assert f_repr(12.1234, 2) == '12'
    assert f_repr(12.1234, 3) == '12.1'
    assert f_repr(12.1234, 4) == '12.12'

    assert f_repr(-12.1234, 0) == '-12'
    assert f_repr(-12.1234, 1) == '-12'
    assert f_repr(-12.1234, 2) == '-12'
    assert f_repr(-12.1234, 3) == '-12.1'
    assert f_repr(-12.1234, 4) == '-12.12'

    assert f_repr(0,0) == '0'
    assert f_repr(0,1) == '0'
    assert f_repr(0,2) == '0'
    assert f_repr(0,3) == '0'


def test_p_repr():
    assert p_repr(12.1234, 0) == '1212%'
    assert p_repr(12.1234, 1) == '1212%'
    assert p_repr(12.1234, 2) == '1212%'
    assert p_repr(12.1234, 3) == '1212%'
    assert p_repr(12.1234, 4) == '1212%'
    assert p_repr(12.1234, 5) == '1212.3%'
    assert p_repr(-12.1234, 0) == '-1212%'
    assert p_repr(-12.1234, 1) == '-1212%'
    assert p_repr(-12.1234, 2) == '-1212%'
    assert p_repr(-12.1234, 3) == '-1212%'
    assert p_repr(-12.1234, 4) == '-1212%'
    assert p_repr(-12.1234, 5) == '-1212.3%'

    assert p_repr(0, 5) == '0%'