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

class TestArtist(unittest.TestCase):
    """ A test class for the Artist module. """
    
    def setUp(self):
        self.artist = api.get_artist("Bon Jovi")
        
    def tearDown(self):
        pass
            
    def testArtistStats(self):
        self.assertEqual(self.artist.stats.listeners, 718040)
        self.assertEqual(self.artist.stats.playcount, 15353197)
    
    def testArtistSimilar(self):
        artists = ['Jon Bon Jovi',
                   'Bryan Adams',
                   'Def Leppard',
                   'Aerosmith',
                   'Whitesnake',
                   'Skid Row',
                   "Guns N' Roses",
                   'Europe']
        self.assertEqual([artist.name for artist in self.artist.similar[:8]], artists)
    
    def testArtistMostSimilar(self):
        self.assertEqual(self.artist.most_similar.name, 'Jon Bon Jovi')
    
    def testArtistTopTags(self):
        tags = ['rock',
                'hard rock',
                'classic rock',
                '80s',
                'hair metal',
                'bon jovi',
                'pop',
                '90s',
                'american',
                'pop rock']
        self.assertEqual([tag.name for tag in self.artist.top_tags[:10]], tags)
    
    def testArtistTopTag(self):
        self.assertEqual(self.artist.top_tag.name, 'rock')
    
    def testArtistBio(self):
        from datetime import datetime
        self.assertEqual(self.artist.bio.summary, 
            'Bon Jovi is a <a href="http://www.last.fm/tag/hardrock" class="bbcode_tag" rel="tag">hardrock</a> band from Sayreville, <span title="Unknown place" class="bbcode_unknown">New Jersey</span>. Fronted by lead singer and namesake Jon Bon Jovi (born John Francis Bongiovi, Jr.), the group originally achieved large-scale success in the 1980s.  Bon Jovi formed in 1983 with lead singer Jon Bon Jovi, guitarist Richie Sambora, keyboardist David Bryan, bassist Alec John Such, and drummer Tico Torres. Other than the departure of Alec John Such in 1994 (which pared the lineup down to a quartet), the lineup has remained the same for the past 26 years. ')
        self.assertEqual(self.artist.bio.published, datetime(2009, 1, 2, 23, 53, 53))
        
    def testArtistEvents(self):
        self.assertEqual(self.artist.events, [api.get_event(642495)])
    
    def testArtistShouts(self):
        shouts = [('jessicahelwig', 'Fri Jan  2 18:44:43 2009'),
                  ('maite72', 'Fri Jan  2 15:04:00 2009'),
                  ('civlenemy', 'Fri Jan  2 11:40:21 2009'),
                  ('Nickpetersen', 'Fri Jan  2 02:49:04 2009'),
                  ('Hard__Candy', 'Thu Jan  1 22:06:13 2009'),
                  ('MissShandy', 'Thu Jan  1 13:08:22 2009'),
                  ('bcnliz', 'Wed Dec 31 18:38:02 2008'),
                  ('-Zelgadis-', 'Mon Dec 29 22:31:24 2008'),
                  ('doeah', 'Mon Dec 29 13:25:32 2008'),
                  ('blhuuh', 'Sun Dec 28 03:40:53 2008')]
        self.assertEqual([(shout.author.name, shout.date.ctime()) for shout in self.artist.shouts[:10]], shouts)
    
    def testArtistRecentShout(self):
        shout = self.artist.recent_shout
        self.assertEqual((shout.author.name, shout.date.ctime()),
                         ('jessicahelwig', 'Fri Jan  2 18:44:43 2009'))
    
    def testArtistSearch(self):
        artists = ['Bon Jovi',
                   'Jon Bon Jovi',
                   'Bon Jovi & Jennifer Nettles',
                   'AC-DC, Def Leppard, Bon Jovi,',
                   'Bon Jovi/Bruce Springsteen',
                   'Bruce Springsteen & Jon Bon Jovi',
                   'Bon Jovi & Sugarland',
                   'Bon Jovi Feat. Big & Rich',
                   'Bon Jovi feat. LeAnn Rimes',
                   'Bon Jovi - Forever Young']
        self.assertEqual([artist.name for artist in api.search_artist("Bon Jovi")[:10]],
                         artists)
    
    def testArtistTopAlbums(self):
        albums = ['Cross Road',
                  'Crush',
                  'Slippery When Wet',
                  'Have a Nice Day',
                  'Lost Highway',
                  'Bounce',
                  'Keep the Faith',
                  'These Days',
                  'New Jersey',
                  'Have a Nice Day + Dvd']
        self.assertEquals([album.name for album in self.artist.top_albums[:10]], albums)
    
    def testArtistTopAlbum(self):
        self.assertEquals(self.artist.top_album.name, 'Cross Road')
    
    def testArtistTopFans(self):
        fans = ['Rockin_Joe',
                'Dante-Santiago',
                'vsc20',
                'Minimalistix',
                'Sparks_and_Fire',
                'Yarzab',
                'CharisL',
                'obracreativa',
                'svart_metall',
                'DJDarkViper']
        self.assertEqual([fan.name for fan in self.artist.top_fans[:10]], fans)
    
    def testArtistTopFan(self):
        self.assertEqual(self.artist.top_fan.name, 'Rockin_Joe')
    
    def testArtistTopTracks(self):
        tracks = ['You Give Love a Bad Name',
                  "Livin' on a Prayer",
                  "It's My Life",
                  'Wanted Dead or Alive',
                  'Always',
                  'Bed of Roses',
                  'Have a Nice Day',
                  'Runaway',
                  'Bad Medicine',
                  'Keep the Faith']
        self.assertEqual([track.name for track in self.artist.top_tracks[:10]], tracks)
        
    def testArtistTopTrack(self):
        self.assertEqual(self.artist.top_track.name, 'You Give Love a Bad Name')
    

apikey = "152a230561e72192b8b0f3e42362c6ff"        
api = Api(apikey, no_cache = True)
   
data = {
    'name': 'Bon Jovi',
    'mbid': '5dcdb5eb-cb72-4e6e-9e63-b7bace604965',
    'url': 'http://www.last.fm/music/Bon+Jovi',
    'image': {'large': 'http://userserve-ak.last.fm/serve/126/24125.jpg',
             'medium': 'http://userserve-ak.last.fm/serve/64/24125.jpg',
             'small': 'http://userserve-ak.last.fm/serve/34/24125.jpg'},
    'streamable': False
}

for k,v in data.iteritems():
    def testFunc(self):
        self.assertEqual(getattr(self.artist, k), v)
    setattr(TestArtist, "testArtist%s" % k.replace('_', ' ').title().replace(' ', ''), testFunc)   
    
test_suite = unittest.TestLoader().loadTestsFromTestCase(TestArtist)

if __name__ == '__main__':
    unittest.main()
