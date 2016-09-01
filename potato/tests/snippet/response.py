# scrapyproject/tests/responses/__init__.py

import os

from scrapy.http import Response, Request
from scrapy.http import TextResponse

def fake_response_from_file( file_name, origin_file=None, url="http://www.google.com" ):
    if origin_file is None:
        origin_file = __file__
    request = Request( url=url )
    if not file_name[0] == '/':
        responses_dir = os.path.dirname( os.path.realpath( origin_file ) )
        file_path = os.path.join( responses_dir, file_name )
    else:
        file_path = file_name

    with open( file_path, 'rb' ) as f:
        file_content = f.read()

    response = TextResponse( url=url, request=request, body=file_content,
                             encoding='utf-8')
    return response
