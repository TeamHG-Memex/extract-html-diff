from itertools import chain
from typing import Union

from lxml.html import HtmlElement, fromstring
import lxml.html.diff as lxml_diff

from .utils import tree_to_string


Html = Union[str, bytes, HtmlElement]


def as_string(
        html: Html, other_html: Html,
        apply_to_siblings: bool=False,
        strip_inline_styles: bool=True
        ) -> str:
    """ Extract diff between two html pages as an html string.
    """
    diff_tree = as_tree(
        html, other_html,
        apply_to_siblings=apply_to_siblings,
        strip_inline_styles=strip_inline_styles)
    return tree_to_string(diff_tree)


def as_tree(
        html: Html, other_html: Html,
        apply_to_siblings: bool=False,
        strip_inline_styles: bool=True
        ) -> HtmlElement:
    """ Extract diff between two html pages as a tree (lxml.html.HtmlElement)
    """
    diff = htmldiff(*[_cleanup(x, strip_inline_styles=strip_inline_styles)
                      for x in [other_html, html]])
    diff_tree = fromstring(diff)
    additions = set(diff_tree.xpath('//ins'))
    deletions = set(diff_tree.xpath('//del'))
    colors = Colors()

    for node in chain(additions, deletions):
        colors.make_green(node)
        if node in additions:
            _apply_recursively(colors.make_green, node)
        for parent in _parents(node):
            if colors.is_green(parent):
                break
            children = parent.getchildren()
            if all(colors.is_green(ch) for ch in children):
                colors.make_green(parent)
            else:
                colors.make_yellow(parent)
                if (apply_to_siblings and
                        any(colors.is_green(ch) for ch in children)):
                    for ch in children:
                        colors.make_yellow(ch)
                        _apply_recursively(colors.make_yellow, ch)

    _remove_uncolored(diff_tree, colors)
    _drop_trees(deletions)
    _drop_tags(additions)

    return diff_tree


def htmldiff(old_html, new_html):
    """ Modified lxml.html.diff.htmldiff:
    * include_hrefs=False - it's hard to fix this " Link: href " stuff,
      and it's not needed (right?)
    * do not do fixup_ins_del_tags, as it re-parses everything
     and we don't need it here
    """
    old_html_tokens = lxml_diff.tokenize(old_html, include_hrefs=False)
    new_html_tokens = lxml_diff.tokenize(new_html, include_hrefs=False)
    result = lxml_diff.htmldiff_tokens(old_html_tokens, new_html_tokens)
    result = ''.join(result).strip()
    return result


def _cleanup(html: Html, strip_inline_styles: bool) -> HtmlElement:
    tree = html if isinstance(html, HtmlElement) else fromstring(html)
    # Do cleanup similar to lxml.html.diff.cleanup_html + comments and styles.
    # It needs to be done since we are passing parsed element here.
    _drop_trees(tree.xpath('//iframe'))
    _drop_trees(tree.xpath('//comment()'))
    _drop_trees(tree.xpath('//head'))
    _drop_trees(tree.xpath('//script'))
    _drop_trees(tree.xpath('//style'))
    _drop_tags(tree.xpath('//ins'))
    _drop_tags(tree.xpath('//del'))
    if strip_inline_styles:
        for node in tree.xpath('//*[@style]'):
            node.attrib.pop('style')
    return tree


def _drop_tags(nodes):
    for node in nodes:
        node.drop_tag()


def _drop_trees(nodes):
    for node in nodes:
        if node.getparent() is not None:
            node.drop_tree()


def _parents(node):
    node = node.getparent()
    while node is not None:
        yield node
        node = node.getparent()


def _remove_uncolored(node, colors):
    for ch in node.getchildren():
        if colors.has_color(ch):
            _remove_uncolored(ch, colors)
        else:
            node.remove(ch)


def _make_children_green(node, colors):
    for ch in node.getchildren():
        if not colors.is_green(ch):
            colors.make_green(ch)
            _make_children_green(ch, colors)

    def fn(ch):
        if not colors.is_yellow(ch):
            colors.make_yellow(ch)
            return True


def _apply_recursively(fn, node):
    for ch in node.getchildren():
        if fn(ch):
            _apply_recursively(fn, ch)


class Colors:
    yellow = 1
    green = 2

    def __init__(self):
        self._node_values = {}

    def make_yellow(self, node):
        return self._make(node, self.yellow)

    def make_green(self, node):
        return self._make(node, self.green)

    def has_color(self, node):
        return node in self._node_values

    def is_yellow(self, node):
        return self._node_values.get(node) == self.yellow

    def is_green(self, node):
        return self._node_values.get(node) == self.green

    def _make(self, node, value):
        old_value = self._node_values.get(node, 0)
        new_value = max(old_value, value)
        self._node_values[node] = new_value
        return new_value != old_value
