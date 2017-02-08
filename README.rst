extract-html-diff: extract difference between two html pages
============================================================

This package allows you to extract a difference between two html pages:
given pages A and B, it will try to extract parts of A that are changed in B.
It uses ``lxml.html.diff`` under the hood. but provides only changed parts as HTML.

It requires Python 3 currently.

License is MIT.

Installaton
-----------

The package is not on PyPI yet, so please install from source::

    pip install git+https://github.com/TeamHG-Memex/extract-html-diff.git


Usage
-----

You can extract diff as text::

    import extract_html_diff

    html = '<div> <h1>My site</h1> <div>My content</div> </div>'
    other_html = '<div> <h1>My site</h1> <div>Other content</div> </div>'

    extract_html_diff.as_string(html, other_html)

this will give you::

    '<div><div>My content</div>  </div>'

You can also get diff as a tree (an ``lxml.etree.Element``) if
you plan to do additional transformations or change serialization::

    extract_html_diff.as_tree(html, other_html)

