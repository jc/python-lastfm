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

class TestGeo(unittest.TestCase):
    """ A test class for the Geo module. """
    
    def setUp(self):
        venue = api.get_venue('tokyo dome')
        self.location = venue.location
        self.country = venue.location.country
        
    def tearDown(self):
        pass
        
    def testLocationLatitude(self):
        self.assertAlmostEqual(self.location.latitude, 35.685, 3)
        
    def testLocationLongitude(self):
        self.assertAlmostEqual(self.location.longitude, 139.7514, 4)    
                
    def testLocationTopTracks(self):
        tracks = [('Viva la Vida', 'Coldplay'),
                 ('Ulysses', 'Franz Ferdinand'),
                 ('Nude', 'Radiohead'),
                 ('Baby cruising Love', 'Perfume'),
                 ('Weird Fishes/Arpeggi', 'Radiohead'),
                 ('Puppy love', 'Perfume'),
                 ('Bodysnatchers', 'Radiohead'),
                 ('Wonderwall', 'Oasis'),
                 ('Jigsaw Falling into Place', 'Radiohead'),
                 ('Invaders Must Die', 'The Prodigy')]
        self.assertEqual(
            [(track.name, track.artist.name) for track in self.location.top_tracks[:10]],
            tracks)
    
    def testLocationTopTrack(self):
        top_track = self.location.top_track
        self.assertEqual((top_track.name, top_track.artist.name), ('Viva la Vida', 'Coldplay'))
        
    def testLocationEvents(self):
        event_ids = [920495, 929525, 828211, 876654, 957549,
                     888895, 948701, 986029, 846323, 951660]
        self.assertEqual([e.id for e in self.location.events[:10]], event_ids)
        
    def testCountryName(self):
        self.assertEqual(self.country.name.lower(), "japan")
        
    def testCountryTopArtists(self):
        artists = ['Perfume', 'Radiohead', 'The Beatles', u'\u304f\u308b\u308a',
                   'Coldplay', 'Oasis', 'Capsule', 'Mr.Children', 'U2', 
                   u'\u5b87\u591a\u7530\u30d2\u30ab\u30eb']
        self.assertEqual([a.name for a in self.country.top_artists[:10]], artists)
        
    def testCountryTopArtist(self):
        self.assertEqual(self.country.top_artist.name, 'Perfume')
        
    def testCountryTopTracks(self):
        tracks = [('Dream Fighter', 'Perfume'),
                  (u'\u5730\u7344\u5148\u751f', u'\u76f8\u5bfe\u6027\u7406\u8ad6'),
                  (u'\u30dd\u30ea\u30ea\u30ba\u30e0', 'Perfume'),
                  (u'\u30c1\u30e7\u30b3\u30ec\u30a4\u30c8\u30fb\u30c7\u30a3\u30b9\u30b3', 'Perfume'),
                  ('Baby cruising Love', 'Perfume'),
                  ('Viva la Vida', 'Coldplay'),
                  (u'\u30c6\u30ec\u6771', u'\u76f8\u5bfe\u6027\u7406\u8ad6'),
                  (u'\u30b7\u30fc\u30af\u30ec\u30c3\u30c8\u30b7\u30fc\u30af\u30ec\u30c3\u30c8', 'Perfume'),
                  (u'\u56db\u89d2\u9769\u547d', u'\u76f8\u5bfe\u6027\u7406\u8ad6'),
                  (u'\u3075\u3057\u304e\u30c7\u30ab\u30eb\u30c8', u'\u76f8\u5bfe\u6027\u7406\u8ad6')]
        self.assertEqual(
            [(track.name, track.artist.name) for track in self.country.top_tracks[:10]],
            tracks)
        
    def testCountryTopTrack(self):
        top_track = self.country.top_track
        self.assertEqual((top_track.name, top_track.artist.name), ('Dream Fighter', 'Perfume'))
   
    def testCountryEvents(self):
        event_ids = [961510, 925636, 959392, 875466, 951038,
                    950520, 957543, 930614, 871240, 857063]
        self.assertEqual([e.id for e in self.country.events[:10]], event_ids)
    
apikey = "152a230561e72192b8b0f3e42362c6ff"        
api = Api(apikey, no_cache = True)
data = {
    'city': "Tokyo",
    'country': api.get_country("Japan"),
    'street': '1-3-61, Koraku, Bunkyo-ku',
    'postal_code': '112-8562'
}

for k,v in data.iteritems():
    def testFunc(self):
        self.assertEqual(getattr(self.location, k), v)
    setattr(TestGeo, "testLocation%s" % k.replace('_', ' ').title().replace(' ', ''), testFunc)
    
test_suite = unittest.TestLoader().loadTestsFromTestCase(TestGeo)

if __name__ == '__main__':
    unittest.main()
