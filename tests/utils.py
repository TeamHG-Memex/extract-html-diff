from lxml.html import fromstring

import extract_html_diff
from extract_html_diff.utils import tree_to_string


def diff_test(html, other_html, expected, **kwargs):
    assert_elements_equal(
        extract_html_diff.as_tree(html, other_html, **kwargs),
        fromstring(expected))


def assert_elements_equal(e1, e2):
    pair = (LazyHtml(e1), LazyHtml(e2))
    assert e1.tag == e2.tag, (e1.tag, e2.tag, pair)
    assert (e1.text or '').strip() == (e2.text or '').strip(), (
        e1.text, e2.text, pair)
    assert (e1.tail or '').strip() == (e2.tail or '').strip(), (
        e1.tail, e2.tail, pair)
    assert e1.attrib == e2.attrib, (e1.attrib, e2.attrib, pair)
    assert len(e1) == len(e2), (len(e1), len(e2), pair)
    for c1, c2 in zip(e1, e2):
        assert_elements_equal(c1, c2)


class LazyHtml:
    """ Lazily computed html repr of an element.
    """
    def __init__(self, el):
        self.el = el

    def __repr__(self):
        return tree_to_string(self.el)
