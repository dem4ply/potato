from scrapy.spiders import Spider
import scrapy
from snippet.lxml import parse

from potato.items import Crunchyroll_article


class Chunchyroll_news( Spider ):
    name = "crunchyroll_new"
    allowed_domains = [ 'www.crunchyroll.com' ]
    start_urls = [ 'http://www.crunchyroll.com/news' ]
    #start_urls = [ 'http://www.crunchyroll.com/anime-news/2016/08/24/kyoto-animation-cuelga-vdeos-subtitulados-para-sordos-de-la-pelcula-de-koe-no-katachi' ]

    def __init__( self, *args, **kargs ):
        super().__init__( *args, **kargs )
        self.craw_all_news = bool( kargs.get( 'craw_all_news', False ) )

    def make_requests_from_url( self, url ):
        return scrapy.Request( url, headers={
            'Accept-Language': "es-ES,es;q=0.8,en;q=0.6"
        } )

    def parse( self, response ):
        if self.craw_all_news:
            previous_url = self.get_previous_url( response )
            yield scrapy.Request( previous_url, callback=self.parse )

        links_articles = self.get_links_of_articles( response )
        for link in links_articles:
            yield scrapy.Request( link, callback=self.parse_article )

    def parse_article( self, response ):
        article = Crunchyroll_article()
        bodys = response.css( 'div.body > div.contents' )
        bodys_text = bodys.xpath( 'string()' ).extract()
        article[ 'title' ] = response.css( '.crunchynews-header a' )\
                                     .xpath( 'string()' ).extract_first()
        article[ 'subtitle' ] = response.xpath( '//h2/@string()' )\
                                        .extract_first()
        article[ 'content' ] = ' '.join( bodys_text )

        article[ 'date' ] = response.css( '.post-date' )\
                                    .xpath( 'text()' ).extract_first()
        article[ 'source' ] = bodys.xpath( './/a/@href' ).extract_first()
        article[ 'link' ] = response.url
        article[ 'tags' ] = self.get_tags_of_article( response )
        article[ 'videos' ] = response.css( '.wpview.wpview-wrap' )\
                                      .xpath( '@data-wpview-text' ).extract()
        return article


    def get_previous_url( self, response ):
        previous_page = response.css( '.previous a' )
        if previous_page:
            previous_url = previous_url.xpath( '@href' ).extract_first()
            previous_url = response.urljoin( previous_url )
            return previous_url

    def get_links_of_articles( self, response ):
        items = response.css( '.news-item h2 a' )
        result = []
        for item in items:
            link = item.xpath( '@href' ).extract_first()
            link = response.urljoin( link )
            result.append( link )
        return result

    def get_tags_of_article( self, response ):
        tags = response.css( '.tags .text-link' ).xpath( '@href|text()' )
        tags = iter(tags.extract())
        return [ { 'name': t[0], 'link': response.urljoin( t[0] ) }
                 for t in zip( tags, tags ) ]
