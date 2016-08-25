# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from urllib import parse


class PotatoPipeline( object ):
    def process_item( self, item, spider ):
        self.clean_body( item )
        self.clean_videos_url( item )
        self.clean_urls( item )
        return item

    def clean_body( self, item ):
        item[ 'content' ] = ' '.join( item[ 'content' ].split() )

    def clean_videos_url( self, item ):
        result = []
        for video_url in item[ 'videos' ]:
            result.append( parse.unquote( video_url ) )
        item[ 'videos' ] = result

    def clean_urls( self, item ):
        item[ 'link' ] = parse.unquote( item[ 'link' ] )
        item[ 'source' ] = parse.unquote( item[ 'source' ] )
