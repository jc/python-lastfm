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

class TestTag(unittest.TestCase):
    """ A test class for the Tag module. """
    
    def setUp(self):
        apikey = "152a230561e72192b8b0f3e42362c6ff"        
        self.api = Api(apikey, no_cache = True)
        self.tag = self.api.get_tag("rock").most_similar
        
    def tearDown(self):
        pass
        
    def testTagName(self):
        self.assertEqual(self.tag.name, "alternative")

    def testTagUrl(self):
        self.assertEqual(self.tag.url, "http://www.last.fm/tag/alternative")
    
    def testTagStreamable(self):
        self.assertEqual(self.tag.streamable, True)
        
    def testTagSimilar(self):
        tags = ['rock',
                'indie',
                'indie rock',
                'alternative rock',
                'seen live',
                'nasty pop',
                'electronic',
                'electronica',
                'kiwi indie niceness',
                'singer-songwriter']
        self.assertEqual([t.name for t in self.tag.similar[:10]], tags)
        
    def testTagMostSimilar(self):
        self.assertEqual(self.tag.most_similar.name, 'rock')

    def testTagTopAlbums(self):
        albums = [('OK Computer', 'Radiohead'),
                  ('Nevermind', 'Nirvana'),
                  ('In Rainbows', 'Radiohead'),
                  ('Absolution', 'Muse'),
                  ('Kid A', 'Radiohead'),
                  ('InTRO', 'Bruno Sanfilippo'),
                  ('A Long And Ugly Road (European edition)', 'June Madrona'),
                  ('The Bends', 'Radiohead'),
                  ('A Rush of Blood to the Head', 'Coldplay'),
                  ('Black Holes And Revelations', 'Muse')]
        self.assertEqual(
            [(album.name, album.artist.name) for album in self.tag.top_albums[:10]],
            albums)
    
    def testTagTopAlbum(self):
        top_album = self.tag.top_album
        self.assertEqual((top_album.name, top_album.artist.name), ('OK Computer', 'Radiohead'))
    
    def testTagTopArtists(self):
        artists = ['Radiohead',
                   'Muse',
                   'Coldplay',
                   'Placebo',
                   'Red Hot Chili Peppers',
                   u'Bj\xf6rk',
                   'Beck',
                   'The Smashing Pumpkins',
                   'Nirvana',
                   'The White Stripes']
        self.assertEqual([artist.name for artist in self.tag.top_artists[:10]], artists)
    
    def testTagTopArtist(self):
        self.assertEqual(self.tag.top_artist.name, 'Radiohead')
    
    def testTagTopTracks(self):
        tracks = [('Nude', 'Radiohead'),
                  ('Karma Police', 'Radiohead'),
                  ('Creep', 'Radiohead'),
                  ('Paranoid Android', 'Radiohead'),
                  ('Starlight', 'Muse'),
                  ('Clocks', 'Coldplay'),
                  ('Wonderwall', 'Oasis'),
                  ("Don't Let Him Waste Your Time", 'Jarvis Cocker'),
                  ('Time Is Running Out', 'Muse'),
                  ('Somebody Told Me', 'The Killers')]
        self.assertEqual(
            [(track.name, track.artist.name) for track in self.tag.top_tracks[:10]],
            tracks)
    
    def testTagTopTrack(self):
        top_track = self.tag.top_track
        self.assertEqual((top_track.name, top_track.artist.name), ('Nude', 'Radiohead'))
    
    def testTagPlaylist(self):
        self.assertEqual(self.tag.playlist.url, 'lastfm://playlist/tag/alternative/freetracks')
    
    def testTagWeeklyChartList(self):
        wcl = [('Sun, 25 May 2008', 'Sun, 01 Jun 2008'),
               ('Sun, 01 Jun 2008', 'Sun, 08 Jun 2008'),
               ('Sun, 08 Jun 2008', 'Sun, 15 Jun 2008'),
               ('Sun, 15 Jun 2008', 'Sun, 22 Jun 2008'),
               ('Sun, 22 Jun 2008', 'Sun, 29 Jun 2008'),
               ('Sun, 29 Jun 2008', 'Sun, 06 Jul 2008'),
               ('Sun, 06 Jul 2008', 'Sun, 13 Jul 2008'),
               ('Sun, 13 Jul 2008', 'Sun, 20 Jul 2008'),
               ('Sun, 20 Jul 2008', 'Sun, 27 Jul 2008'),
               ('Sun, 27 Jul 2008', 'Sun, 03 Aug 2008')]
        self.assertEqual(
            [
                (
                    wc.start.date().strftime('%a, %d %b %Y'),
                    wc.end.date().strftime('%a, %d %b %Y')
                )
                for wc in self.tag.weekly_chart_list[:10]
            ],
            wcl
            )
    
    def testTagGetWeeklyArtistChart(self):
        artists = [('Radiohead', 1199680000),
                   ('Coldplay', 1000771456),
                   ('Muse', 777053504),
                   ('Placebo', 574809984),
                   ('The Killers', 549784640),
                   ('The Smashing Pumpkins', 523733376),
                   ('The Cure', 503786272),
                   ('Gorillaz', 488720000),
                   ('Beck', 474790016),
                   ('Weezer', 448279168)]
        wc = self.tag.weekly_chart_list[0]
        self.assertEqual(
            [(artist.name, artist.stats.weight)
             for artist in self.tag.get_weekly_artist_chart(wc.start, wc.end).artists[:10]],
            artists)
    
    def testTagGetTopTags(self):
        tags = ['rock',
                'seen live',
                'alternative',
                'indie',
                'electronic',
                'pop',
                'metal',
                'female vocalists',
                'alternative rock',
                'classic rock']
        self.assertEqual([tag.name for tag in self.api.get_global_top_tags()[:10]], tags)
    
    def testTagSearch(self):
        tags = ['alternative',
                'alternative rock',
                'alternative metal',
                'alternative pop',
                'alternative dance',
                'alternative rap',
                'alternative country',
                'adult alternative',
                'alternative hip-hop',
                'alternative folk']
        self.assertEqual([tag.name for tag in self.api.search_tag('alternative')[:10]], tags)
    
test_suite = unittest.TestLoader().loadTestsFromTestCase(TestTag)

if __name__ == '__main__':
    unittest.main()
