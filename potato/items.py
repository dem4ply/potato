# -*- coding: utf-8 -*-
import scrapy
import json
import requests


class Crunchyroll_article( scrapy.Item ):
    link  = scrapy.Field()
    title = scrapy.Field()
    subtitle = scrapy.Field()
    date = scrapy.Field()
    content = scrapy.Field()
    source = scrapy.Field()
    tags = scrapy.Field()
    videos = scrapy.Field()

    def save( self ):
        d = dict( self )
        str_json = json.dumps( d )
        response = requests.post(
            'http://magi:8000/crunchiroll/newspaper/', data=str_json,
            headers={ 'content-type': 'application/json' } )
        return response.status_code == 204
