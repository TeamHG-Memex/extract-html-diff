import extract_html_diff

from .utils import diff_test


def test_as_string():
    html = '<div> <h1>My site</h1> <div>My content</div> </div>'
    other_html = '<div> <h1>My site</h1> <div>Other content</div> </div>'
    assert extract_html_diff.as_string(html, other_html) == \
        '<div><div>My content</div> </div>'


def test_as_tree():
    diff_test(
        '<div> <h1>My site</h1> <div>My content</div> </div>',
        '<div> <h1>My site</h1> <div>Other content</div> </div>',
        '<div><div>My content</div></div>')


def test_ignore_comments():
    diff_test(
        '<div><!-- <div>foo</div> --><p>bar</p><p>foo</p></div>',
        '<div><!-- <div>zoo</div> --><p>bar</p><p>goo</p></div>',
        '<div><p>foo</p></div>')


def test_full_html():
    diff_test(
        '<html><body>zoo</body></html>',
        '<html><body>goo</body></html>',
        '<div>zoo</div>')


def test_ignore_style():
    diff_test(
        '<html><body><style>aa</style> zoo</body></html>',
        '<html><body><style>bb</style> goo</body></html>',
        '<div>zoo</div>')


def test_ins_del():
    diff_test(
        '<div><div><del>bb</del></div> <div>cc</div> <div><del>dd</del></div></div>',
        '<div><div><del>bb</del></div> <div>c1</div> <div><del>d1</del></div></div>',
        '<div><div>cc</div> <div>dd</div></div>')
