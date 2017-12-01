import pkg_resources


def load_html(name):
    return pkg_resources.resource_string(__name__, "/".join(("html", name))).decode("utf-8")
