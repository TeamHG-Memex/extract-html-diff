extract-html-diff: extract difference between two html pages
============================================================

.. image:: https://img.shields.io/travis/TeamHG-Memex/extract-html-diff/master.svg
   :target: http://travis-ci.org/TeamHG-Memex/extract-html-diff
   :alt: Build Status

.. image:: http://codecov.io/github/TeamHG-Memex/extract-html-diff/coverage.svg?branch=master
   :target: http://codecov.io/github/TeamHG-Memex/extract-html-diff?branch=master
   :alt: Code Coverage

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

You can also get diff as a tree (an ``lxml.html.HtmlElement``) if
you plan to do additional transformations or change serialization::

    extract_html_diff.as_tree(html, other_html)

You can pass input html as ``str`` or ``bytes``
(it will be parsed with ``lxml.html.fromstring`` in this case), or as an already parsed
``lxml.html.HtmlElement``.
