from scrapy.spiders import Spider
import scrapy
from snippet.lxml import parse

from potato.items import Crunchyroll_new


class Chunchyroll( Spider ):
    name = "chunchyroll"
    allowed_domains = [ 'http://www.crunchyroll.com' ]
    start_urls = [ 'http://www.crunchyroll.com/news' ]

    def make_requests_from_url( self, url ):
        return scrapy.Request( url, headers={
            'Accept-Language': "es-ES,es;q=0.8,en;q=0.6"
        } )

    def parse( self, response ):
        items = response.css( '.news-item h2 a' )
        for item in items:
            link = item.xpath( '@href' ).extract_first()
            link = response.urljoin( link )
            text = item.xpath( 'text()' ).extract_first()
            new = Crunchyroll_new()
            new[ 'link' ] = link
            new[ 'title' ] = text
            yield new
