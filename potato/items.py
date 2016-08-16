# -*- coding: utf-8 -*-
import scrapy
import json
import requests


class Crunchyroll_new( scrapy.Item ):
    link  = scrapy.Field()
    title = scrapy.Field()

    def save( self ):
        d = dict( self )
        response = requests.post( 'http://magi:8000/papernews/test/',
                                  data=json.dumps( d ),
                                  headers={ 'content-type': 'application/json' } )
        return response.status_code == 204
