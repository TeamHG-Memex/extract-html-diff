import lxml.html


def tree_to_string(tree, **kwargs) -> str:
    return (lxml.html.tostring(tree, encoding='utf8', **kwargs)
            .decode('utf8'))


