import pytest
from hypothesis import given, strategies as st

def add(a: int, b: int) -> int:
    return a + b

@pytest.mark.parametrize("a,b,expected", [(1,2,3), (-1,1,0)])
def test_parametrize(a, b, expected):
    assert add(a, b) == expected

def test_pytest_mock(mocker):
    fake = mocker.Mock()
    fake.return_value = 42
    assert fake() == 42

@given(st.integers(), st.integers())
def test_property_based(x, y):
    assert add(x, y) == add(y, x)
