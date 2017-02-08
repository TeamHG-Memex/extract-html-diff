import extract_html_diff
from extract_html_diff.utils import tree_to_string


def test_as_string():
    html = '<div> <h1>My site</h1> <div>My content</div> </div>'
    other_html = '<div> <h1>My site</h1> <div>Other content</div> </div>'
    assert extract_html_diff.as_string(html, other_html) == \
        '<div><div>My content</div>  </div>'


def test_as_tree():
    html = '<div> <h1>My site</h1> <div>My content</div> </div>'
    other_html = '<div> <h1>My site</h1> <div>Other content</div> </div>'
    assert tree_to_string(extract_html_diff.as_tree(html, other_html)) == \
           '<div><div>My content</div>  </div>'
