#!/usr/bin/env python

__author__ = "Abhinav Sarkar <abhinav@abhinavsarkar.net>"
__version__ = "0.2"
__license__ = "GNU Lesser General Public License"

import unittest
import datetime
import sys, os

from wsgi_intercept.urllib2_intercept import install_opener
import wsgi_intercept
from wsgi_test_app import create_wsgi_app

install_opener()
wsgi_intercept.add_wsgi_intercept('ws.audioscrobbler.com', 80, create_wsgi_app)
    
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from lastfm import Api

class TestAlbum(unittest.TestCase):
    """ A test class for the Album module. """
    
    def setUp(self):
        self.album = api.get_album("Supersonic", "Oasis")
        
    def tearDown(self):
        pass
        
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
            [(album.name, album.artist.name) for album in api.search_album("paradice")[:10]],
            albums
        )

apikey = "152a230561e72192b8b0f3e42362c6ff"        
api = Api(apikey, no_cache = True)

data = {
    'name': "Supersonic",
    'artist': api.get_artist("Oasis"),
    'id': 2038492,
    'mbid': '2c2a24de-67b6-483b-b597-9c6b7891ba90',
    'url': 'http://www.last.fm/music/Oasis/Supersonic',
    'release_date': datetime.datetime(1994, 7, 28, 0, 0),
    'image': {
              'extralarge': 'http://userserve-ak.last.fm/serve/300x300/23049597.jpg',
              'large': 'http://userserve-ak.last.fm/serve/174s/23049597.jpg',
              'medium': 'http://userserve-ak.last.fm/serve/64s/23049597.jpg',
              'small': 'http://userserve-ak.last.fm/serve/34s/23049597.jpg'
        }
}
        
for k,v in data.iteritems():
    def testFunc(self):
        self.assertEqual(getattr(self.album, k), v)
    setattr(TestAlbum, "testAlbum%s" % k.replace('_', ' ').title().replace(' ', ''), testFunc)   
    
test_suite = unittest.TestLoader().loadTestsFromTestCase(TestAlbum)

if __name__ == '__main__':
    unittest.main()
