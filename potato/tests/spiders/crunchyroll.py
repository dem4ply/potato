import unittest

from potato.spiders.crunchyroll import Chunchyroll_news
from potato.tests.snippet.response import fake_response_from_file


class Test_crunchyroll( unittest.TestCase ):

    def setUp( self ):
        self.spider = Chunchyroll_news()

    def test_response_article( self, response=None, test_video=True ):
        if response is None:
            response = fake_response_from_file(
                    'crunchyroll_without_video.html',
                    origin_file=__file__ )

        result = self.spider.parse_article( response )

        self.assertTrue( result[ 'title' ] )
        self.assertIn( 'subtitle', result )
        self.assertTrue( result[ 'date' ] )
        self.assertTrue( result[ 'content' ] )
        self.assertTrue( result[ 'tags' ] )
        if test_video:
            self.assertFalse( result[ 'videos' ] )
        return result

    def test_response_article_with_video( self ):
        response = fake_response_from_file( 'crunchyroll_with_video.html',
                                            origin_file=__file__ )
        result = self.test_response_article( response=response,
                                             test_video=False )

        self.assertTrue( result[ 'videos' ] )
        self.assertEqual( len( result[ 'videos' ] ), 1 )

        return result

    def test_response_article_weird_video( self ):
        response = fake_response_from_file( 'crunchyroll_article_video_fail.html',
                                            origin_file=__file__ )
        result = self.test_response_article( response=response,
                                             test_video=False )

        self.assertTrue( result[ 'videos' ] )
        self.assertEqual( len( result[ 'videos' ] ), 2 )
        #print( result[ 'videos' ] )

        return result

    def test_parse_all_news( self ):
        response = fake_response_from_file( 'crunchyroll_news.html',
                                            origin_file=__file__ )
        self.spider.craw_all_news = True
        result = self.spider.parse( response )
        first = next( result )
        self.assertTrue(
            first.url.startswith( 'http://www.crunchyroll.com/news/date/' ) )
        for page in result:
            is_good = page.url\
                .startswith( 'http://www.crunchyroll.com/anime-news/' )
            self.assertTrue( is_good )

    def test_parse_news( self ):
        response = fake_response_from_file( 'crunchyroll_news.html',
                                            origin_file=__file__ )
        result = self.spider.parse( response )
        for page in result:
            is_good = page.url\
                .startswith( 'http://www.crunchyroll.com/anime-news/' )
            self.assertTrue( is_good )
