import lxml.html
from io import StringIO


def parse( page_string):
    return lxml.html.fromstring( page_string )
