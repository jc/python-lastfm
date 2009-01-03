#!/usr/bin/env python

__author__ = "Abhinav Sarkar <abhinav@abhinavsarkar.net>"
__version__ = "0.2"
__license__ = "GNU Lesser General Public License"

import unittest
import datetime
import sys

from wsgi_intercept.urllib2_intercept import install_opener
import wsgi_intercept
from wsgi_test_app import create_wsgi_app

install_opener()
wsgi_intercept.add_wsgi_intercept('ws.audioscrobbler.com', 80, create_wsgi_app)
    
sys.path.append("..")
from lastfm import Api

class TestAlbum(unittest.TestCase):
    """ A test class for the Album module. """
    
    def setUp(self):
        apikey = "152a230561e72192b8b0f3e42362c6ff"        
        self.api = Api(apikey, no_cache = True)
        self.album = self.api.get_album("Oasis", "Supersonic")
        
    def tearDown(self):
        pass
        
    def testAlbumName(self):
        self.assertEqual(self.album.name, "Supersonic")

    def testAlbumArtist(self):
        self.assertEqual(self.album.artist.name, "Oasis")
    
    def testAlbumId(self):
        self.assertEqual(self.album.id, 2038492)
        
    def testAlbumMbid(self):
        mbid = '2c2a24de-67b6-483b-b597-9c6b7891ba90'
        self.assertEqual(self.album.mbid, mbid)
        
    def testAlbumUrl(self):
        url = 'http://www.last.fm/music/Oasis/Supersonic'
        self.assertEqual(self.album.url, url)
        
    def testAlbumReleaseDate(self):
        date = datetime.datetime(1994, 7, 28, 0, 0)
        self.assertEqual(self.album.release_date, date)
        
    def testAlbumImage(self):
        self.assertEqual(self.album.image['small'], "http://userserve-ak.last.fm/serve/34/11846565.jpg")
        self.assertEqual(self.album.image['medium'], "http://userserve-ak.last.fm/serve/64/11846565.jpg")
        self.assertEqual(self.album.image['large'], "http://userserve-ak.last.fm/serve/174s/11846565.jpg")
        self.assertEqual(self.album.image['extralarge'], "http://userserve-ak.last.fm/serve/300x300/11846565.jpg")
    
    def testAlbumStats(self):
        self.assertEqual(self.album.stats.listeners, 14286)
        self.assertEqual(self.album.stats.playcount, 39594)
    
    def testAlbumTopTags(self):
        pass
    
    def testAlbumTopTag(self):
        pass
    
    def testAlbumPlaylist(self):
        self.assertEqual(self.album.playlist.url, "lastfm://playlist/album/2038492")
        
    def testAlbumSearch(self):
        albums = [('return to paradice', 'Waldeck'),
                 ('Paradice is Empty', 'I-Disagree'),
                 ('Paradice', 'The Mods'),
                 ('paradice slave', 'flower of flesh and blood'),
                 ('return to paradice', 'Flunk'),
                 ('return to paradice', 'Nostalgia 77'),
                 ('return to paradice', 'Katalyst'),
                 ('return to paradice', 'Ennio Morricone'),
                 ('return to paradice', 'Cornucopia'),
                 ('return to paradice', 'Lost Balance')]
        self.assertEqual(
            [(album.name, album.artist.name) for album in self.api.search_album("paradice")[:10]],
            albums
        )

test_suite = unittest.TestLoader().loadTestsFromTestCase(TestAlbum)

if __name__ == '__main__':
    unittest.main()
