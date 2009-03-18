#!/usr/bin/env python

__author__ = "Abhinav Sarkar <abhinav@abhinavsarkar.net>"
__version__ = "0.2"
__license__ = "GNU Lesser General Public License"

import unittest
import sys, os

from wsgi_intercept.urllib2_intercept import install_opener
import wsgi_intercept
from wsgi_test_app import create_wsgi_app

install_opener()
wsgi_intercept.add_wsgi_intercept('ws.audioscrobbler.com', 80, create_wsgi_app)
    
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from lastfm import Api

class TestPlaylist(unittest.TestCase):
    """ A test class for the Geo module. """
    
    def setUp(self):
        apikey = "152a230561e72192b8b0f3e42362c6ff"        
        self.api = Api(apikey, no_cache = True)
        self.playlist = self.api.get_playlist('lastfm://playlist/album/2287667')
        
    def tearDown(self):
        pass
        
    def testPlaylistUrl(self):
        self.assertEqual(self.playlist.url, 'lastfm://playlist/album/2287667')
        
#    def testPlaylistData(self):
#        data = """<?xml version="1.0" encoding="utf-8"?>
#<lfm status="ok">
#<playlist version="1" xmlns="http://xspf.org/ns/0/">
#<title>Bon Jovi - Have a Nice Day</title>
#<annotation>Previews for Bon Jovi - Have a Nice Day</annotation>
#<creator>http://www.last.fm/music/Bon+Jovi/Have+a+Nice+Day</creator>
#<date>2009-03-04T09:49:28</date>
#<trackList>
#            <track>
#        <title>Have a Nice Day</title>
#        <identifier>http://www.last.fm/music/Bon+Jovi/_/Have+a+Nice+Day</identifier>
#        <album>Have a Nice Day</album>
#        <creator>Bon Jovi</creator>
#        <duration>228000</duration>
#        <info>http://www.last.fm/music/Bon+Jovi/_/Have+a+Nice+Day</info>
#        <image>http://userserve-ak.last.fm/serve/126/8750501.jpg</image>    </track>
#</trackList>
#</playlist>
#</lfm>
#"""
#        self.assertEqual(self.playlist.data, data)
        
test_suite = unittest.TestLoader().loadTestsFromTestCase(TestPlaylist)

if __name__ == '__main__':
    unittest.main()
