import unittest

from potato.pipelines import Crunchyroll_clean
from potato.tests.snippet.response import fake_response_from_file


class Test_crunchyroll_clean_pipeline( unittest.TestCase ):

    def test_clean_body( self ):
        item = {
            'content':
                'Bandai Namco\xa0ha anunciado\xa0Kingdom: Seven '
                'Flags,\xa0un juego de estrategia basado en el manga y '
                'anime Kingdom que llegará a iOS y Android como '
                'free-to-play.\r\n\xa0\r\n'
            }
        clean = ( 'Bandai Namco ha anunciado Kingdom: Seven Flags, un juego '
                  'de estrategia basado en el manga y anime Kingdom que '
                  'llegará a iOS y Android como free-to-play.' )
        pipe = Crunchyroll_clean()
        pipe.clean_body( item )

        self.assertEqual( item[ 'content' ], clean )


        'http://www.google.com/newsfeed/tag/videojuegos'

    def test_clean_video_url( self ):
        pipe = Crunchyroll_clean()
        item = {
            'videos': [
                'https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3DPmuGYvefGmY',
                'https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3DPmuGYvefGmY' ]
        }
        clean = [
            { 'link': 'https://www.youtube.com/watch?v=PmuGYvefGmY', },
            { 'link': 'https://www.youtube.com/watch?v=PmuGYvefGmY', },
        ]
        pipe.clean_videos_url( item )
        self.assertEqual( item[ 'videos' ], clean )

    def test_clean_urls( self ):
        pipe = Crunchyroll_clean()
        item = {
            'source': 'http%3A%2F%2Fwww.blogiswar.net%2F',
            'link': 'http%3A%2F%2Fwww.blogiswar.net%2F',
        }
        clean = {
            'source': 'http://www.blogiswar.net/',
            'link': 'http://www.blogiswar.net/',
        }
        pipe.clean_urls( item )
        self.assertEqual( item, clean )

    def test_clean_urls_no_fail_with_none_source( self ):
        pipe = Crunchyroll_clean()
        item = {
            'source': None,
            'link': 'http%3A%2F%2Fwww.blogiswar.net%2F',
        }
        clean = {
            'source': None,
            'link': 'http://www.blogiswar.net/',
        }
        pipe.clean_urls( item )
        self.assertEqual( item, clean )
