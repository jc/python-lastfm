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

class TestGroup(unittest.TestCase):
    """ A test class for the Group module. """
    
    def setUp(self):
        apikey = "152a230561e72192b8b0f3e42362c6ff"        
        self.api = Api(apikey, no_cache = True)
        self.group = self.api.get_group('Rock')
        
    def tearDown(self):
        pass
        
    def testGroupName(self):
        self.assertEqual(self.group.name, 'Rock')
        
    def testGroupMembers(self):
        members = ['Alaa10', 'ilovemusix', 'Bartuu', 'ABeyers', 'kaique1002',
                   'Thug4Life2Da', 'Fishuturek', 'JapanesBoy', 'rubenius90',
                   '230688']
        self.assertEqual([m.name for m in self.group.members[:10]], members)
        
    def testGroupWeeklyChartList(self):
        wcl = [('Sun, 24 Sep 2006', 'Sun, 01 Oct 2006'),
              ('Sun, 01 Oct 2006', 'Sun, 08 Oct 2006'),
              ('Sun, 08 Oct 2006', 'Sun, 15 Oct 2006'),
              ('Sun, 15 Oct 2006', 'Sun, 22 Oct 2006'),
              ('Sun, 22 Oct 2006', 'Sun, 29 Oct 2006'),
              ('Sun, 29 Oct 2006', 'Sun, 05 Nov 2006'),
              ('Sun, 05 Nov 2006', 'Sun, 12 Nov 2006'),
              ('Sun, 12 Nov 2006', 'Sun, 19 Nov 2006'),
              ('Sun, 19 Nov 2006', 'Sun, 26 Nov 2006'),
              ('Sun, 26 Nov 2006', 'Sun, 03 Dec 2006')]
        self.assertEqual(
            [
                (
                    wc.start.date().strftime('%a, %d %b %Y'),
                    wc.end.date().strftime('%a, %d %b %Y')
                )
                for wc in self.group.weekly_chart_list[:10]
            ],
            wcl
            )
    
    def testGroupGetWeeklyArtistChart(self):
        artists = ['Red Hot Chili Peppers',
                     'Led Zeppelin',
                     'Metallica',
                     'Pink Floyd',
                     'Queen',
                     "Guns N' Roses",
                     'AC/DC',
                     'The Beatles',
                     'Nirvana',
                     'Muse']
        wc = self.group.weekly_chart_list[0]
        self.assertEqual(
            [artist.name
             for artist in self.group.get_weekly_artist_chart(wc.start, wc.end).artists[:10]],
            artists)
        
    def testGroupGetWeeklyAlbumChart(self):
        albums = [('By the Way', 'Red Hot Chili Peppers', 48),
                     ('Toxicity', 'System of a Down', 48),
                     ('Stadium Arcadium', 'Red Hot Chili Peppers', 43),
                     ('OK Computer', 'Radiohead', 41),
                     ('Absolution', 'Muse', 39),
                     ('Californication', 'Red Hot Chili Peppers', 38),
                     ('Back in Black', 'AC/DC', 37),
                     ('Black Holes And Revelations', 'Muse', 37),
                     ('Appetite for Destruction', "Guns N' Roses", 35),
                     ('Meteora', 'Linkin Park', 35)]
        wc = self.group.weekly_chart_list[0]
        self.assertEqual(
             [(album.name, album.artist.name, album.stats.playcount)
                for album in self.group.get_weekly_album_chart(wc.start, wc.end).albums[:10]],
            albums)
        
    def testGroupGetWeeklyTrackChart(self):
        tracks = [('Stairway to Heaven', 'Led Zeppelin', 36),
                     ('Back in Black', 'AC/DC', 34),
                     ('Enter Sandman', 'Metallica', 33),
                     ('Dani California', 'Red Hot Chili Peppers', 33),
                     ('Bohemian Rhapsody', 'Queen', 31),
                     ('Welcome to the Jungle', "Guns N' Roses", 30),
                     ('Supermassive Black Hole', 'Muse', 30),
                     ('Wonderwall', 'Oasis', 29),
                     ('Run to the Hills', 'Iron Maiden', 28),
                     ('November Rain', "Guns N' Roses", 28)]
        wc = self.group.weekly_chart_list[0]
        self.assertEqual(
             [(track.name, track.artist.name, track.stats.playcount)
                for track in self.group.get_weekly_track_chart(wc.start, wc.end).tracks[:10]],
            tracks)
        
    def testGroupGetWeeklyTagChart(self):
        tags = [('classic rock', 156),
                ('rock', 154), 
                ('alternative', 130), 
                ('british', 112), 
                ('alternative rock', 110), 
                ('hard rock', 78), 
                ('metal', 63), 
                ('psychedelic', 61), 
                ('thrash metal', 54), 
                ('heavy metal', 47)]
        wc = self.group.weekly_chart_list[0]
        self.assertEqual(
             [(tag.name, tag.stats.count)
                for tag
                in self.group.get_weekly_tag_chart(wc.start, wc.end).tags[:10]],
            tags)
            
test_suite = unittest.TestLoader().loadTestsFromTestCase(TestGroup)

if __name__ == '__main__':
    unittest.main()
