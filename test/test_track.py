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

class TestTrack(unittest.TestCase):
    """ A test class for the Geo module. """
    def setUp(self):
        self.track = api.get_track('Lithium', 'Evanescence')
        
    def tearDown(self):
        pass
    
    def testTrackStats(self):
        self.assertEqual(self.track.stats.listeners, 159098)
        self.assertEqual(self.track.stats.playcount, 1281349)
        
    def testTrackWiki(self):
        from datetime import datetime
        self.assertEqual(self.track.wiki.summary, 
            "Written by: A. Lee  Amy Lee has been quoted saying the song is about losing the comfort of sorrow. Lithium is a mood stabilizer that would take away the sorrow that the writer holds inside and she is not ready to let go of it. She has lived with sorrow so long that losing it now would be like losing a part of herself. That is what the whole refrain is about: &quot;Lithium, Don't want to lock myself up inside, Lithium, Don't want to forget what it feels without, Lithium, I want to stay in love with my sorrow.")
        self.assertEqual(self.track.wiki.published, datetime(2009, 2, 4, 8, 20, 59))
        
    def testTrackSimilar(self):
        tracks = [('Here Without You', '3 Doors Down'),
                     ('Wicked Game', 'HIM'),
                     ('In the Shadows', 'The Rasmus'),
                     ('Driven Under', 'Seether'),
                     ('Fine Again', 'Seether'),
                     ('Rip Out the Wings of a Butterfly', 'HIM'),
                     ('Outro', 'Breaking Benjamin'),
                     ('So Far Away', 'Staind'),
                     ('Outside', 'Staind'),
                     ('Guilty', 'The Rasmus')]
        self.assertEqual([(s.name, s.artist.name) for s in self.track.similar[:10]], tracks)
        
    def testTrackMostSimilar(self):
        most_similar = self.track.most_similar
        self.assertEqual((most_similar.name, most_similar.artist.name),
                         ('Here Without You', '3 Doors Down'))
        
    def testTrackTopFans(self):
        fans = ['danyzinhalee_ev', 'acandec', 'hawkieye', 'Nostress1991',
                'jfinner1', 'mychaelbs', 'vince88enzo', 'cuate_julian',
                'Slempa', 'fuckin_killa']
        self.assertEqual([f.name for f in self.track.top_fans[:10]], fans)
        
    def testTrackTopFan(self):
        self.assertEqual(self.track.top_fan.name, 'danyzinhalee_ev')
        
    def testTrackTopTags(self):
        tags = ['rock', 'Gothic Rock', 'Gothic', 'Evanescence', 'female vocalists',
                'alternative', 'metal', 'Gothic Metal', 'alternative rock', 'lithium']
        self.assertEqual([t.name for t in self.track.top_tags[:10]], tags)
    
    def testTrackTopTag(self):
        self.assertEqual(self.track.top_tag.name, 'rock')
        
    def testTrackSearch(self):
        tracks = [('Plug In Baby', 'Muse'),
                     ('Tell Me Baby', 'Red Hot Chili Peppers'),
                     ('Combat Baby', 'Metric'),
                     ('Hey Baby', 'No Doubt'),
                     ('Cry Baby Cry', 'The Beatles'),
                     ('Find My Baby', 'Moby'),
                     ('Nobody Puts Baby in the Corner', 'Fall Out Boy'),
                     ('Baby Fratelli', 'The Fratellis'),
                     ("I Can't Quit You Baby", 'Led Zeppelin'),
                     ('Baby Britain', 'Elliott Smith')]
        self.assertEqual([(t.name, t.artist.name) for t 
                          in list(api.search_track('baby')[:10])], tracks)

apikey = "152a230561e72192b8b0f3e42362c6ff"        
api = Api(apikey, no_cache = True)
        
data = {
    'name': 'Lithium',
    'mbid': '',
    'url': 'http://www.last.fm/music/Evanescence/_/Lithium',
    'duration': 223000,
    'streamable': True,
    'full_track': False,
    'artist': api.get_artist('Evanescence'),
    'album': api.get_album('The Open Door', 'Evanescence'),
    'position': 4,
    'image': {}
}
for k,v in data.iteritems():
    def testFunc(self):
        self.assertEqual(getattr(self.track, k), v)
    setattr(TestTrack, "testTrack%s" % k.replace('_', ' ').title().replace(' ', ''), testFunc)
                
test_suite = unittest.TestLoader().loadTestsFromTestCase(TestTrack)

if __name__ == '__main__':
    unittest.main()
