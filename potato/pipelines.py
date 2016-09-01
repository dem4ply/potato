# -*- coding: utf-8 -*-
from urllib import parse
from potato.items import Crunchyroll_article


class Crunchyroll_clean( object ):
    def process_item( self, item, spider ):
        if isinstance( item, Crunchyroll_article ):
            self.clean_body( item )
            self.clean_videos_url( item )
            self.clean_urls( item )
        return item

    def clean_body( self, item ):
        item[ 'content' ] = ' '.join( item[ 'content' ].split() )

    def clean_videos_url( self, item ):
        result = []
        for video_url in item[ 'videos' ]:
            url = parse.unquote( video_url )
            result.append( { 'link': url } )
        item[ 'videos' ] = result

    def clean_urls( self, item ):
        item[ 'link' ] = parse.unquote( item[ 'link' ] )
        if item[ 'source' ]:
            item[ 'source' ] = parse.unquote( item[ 'source' ] )

