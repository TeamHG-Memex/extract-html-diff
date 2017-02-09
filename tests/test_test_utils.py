import pytest
from lxml.html import fragment_fromstring

from .utils import assert_elements_equal


def test_assert_elements_equal():
    assert_elements_equal(
        fragment_fromstring('<div>foo<a href="bar" class="baz"><br/></div>'),
        fragment_fromstring('<div>foo <a class="baz" href="bar"> <br/></div>'))
    with pytest.raises(AssertionError):
        assert_elements_equal(
            fragment_fromstring('<div><div>foo</div></div>'),
            fragment_fromstring('<div>foo</div>'))
    with pytest.raises(AssertionError):
        assert_elements_equal(
            fragment_fromstring('<div><div>foo</div></div>'),
            fragment_fromstring('<div><div>food</div></div>'))
    with pytest.raises(AssertionError):
        assert_elements_equal(
            fragment_fromstring('<div class="foo">foo</div>'),
            fragment_fromstring('<div class="foo" id="bar">foo</div>'))
    with pytest.raises(AssertionError):
        assert_elements_equal(
            fragment_fromstring('<div class="foo">foo</div>'),
            fragment_fromstring('<div class="food">foo</div>'))
