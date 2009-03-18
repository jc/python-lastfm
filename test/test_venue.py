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

class TestVenue(unittest.TestCase):
    """ A test class for the Geo module. """
    
    def setUp(self):
        self.venue = api.get_venue('tokyo dome')
        
    def tearDown(self):
        pass
    
    def testVenueLocation(self):
        self.assertEqual(self.venue.location.city, 'Tokyo')
        
    def testVenueEvents(self):
        self.assertEqual([e.id for e in self.venue.events[:5]],
                         [942975, 942976, 942986, 942991, 942993])
        
    def testVenuePastEvents(self):
        self.assertEqual([e.id for e in self.venue.past_events[:5]],
                         [845504, 867074, 845502, 845499, 722964])
        
    def testVenueSearch(self):
        venues = [8881428, 8887127, 8894829, 8899152, 8938738,
                  8778901, 8779255, 8779726, 8802306, 8781168]
        self.assertEqual([venue.id for venue 
                          in list(api.search_venue('stadium')[:10])], venues)
                
apikey = "152a230561e72192b8b0f3e42362c6ff"        
api = Api(apikey, no_cache = True)
        
data = {
    'id': 8780357,
    'name': 'Tokyo Dome',
    'url': 'http://www.last.fm/venue/8780357'
}
for k,v in data.iteritems():
    def testFunc(self):
        self.assertEqual(getattr(self.venue, k), v)
    setattr(TestVenue, "testVenue%s" % k.replace('_', ' ').title().replace(' ', ''), testFunc)
        
test_suite = unittest.TestLoader().loadTestsFromTestCase(TestVenue)

if __name__ == '__main__':
    unittest.main()
