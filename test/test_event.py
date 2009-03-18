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

class TestEvent(unittest.TestCase):
    """ A test class for the Event module. """
    
    def setUp(self):
        self.event = api.get_event(216156)
        
    def tearDown(self):
        pass
                
    def testEventArtists(self):
        artists = ['Aerosmith']
        self.assertEqual([artist.name for artist in self.event.artists], artists)
        
    def testEventHeadliner(self):
        self.assertEqual(self.event.headliner.name, 'Aerosmith')
        
    def testEventStats(self):
        self.assertEqual(self.event.stats.attendance, 48)
        self.assertEqual(self.event.stats.reviews, 1)
        
    def testEventShouts(self):
        shouts = [('Aeromaniac21280',
                   'It was a brillian show still jealous at some ppl who could meet them  video of joe perry banging the guitar in youtube, in between u will see a devils hand with the thorny black heavy metal wrist band, that hand IS MINE LOL!!!'),
                   ('ncortizone5', 'brilliant show!!'),
                   ('drunkenpunk', '@Ninja ; just take a look at my charts...'),
                   ('sanirudha',
                   'I won the Guitar...Thanks guys. I know you had to bear us. Can understand the pain of waiting. [But ours was only 3 min performance] Worth all the shit I did for past month to qualify. Thanks anyways, I will post the photos of the guitar very soon!'),
                   ('nano0101', 'Which band is gonna open for them???'),
                   ('funndude', 'looks like drunkenpunk is not the only one drunk :-)'),
                   ('buttrflyeffect',
                   'as we say in namma beelore -  this is like, AWSUM! like, hello? like, aerosmith, like TOTALLY rocks..! like, i will SOOOOOO TO-TAH-LEE bee there! haha that sounds so lame..\nI *heart* Steven Tyler.\nAnd Aerosmith.\nAnd Jaded. \nAnd all things Aerosmith. :)'),
                   ('cvn2nvc', 'drunkenpunk is drunk.... aerosmith rocks!'),
                   ('funndude', 'I guess I am happier with Aerosmith than Absolutely No One'),
                   ('NinjaRocker', '@drunkenpunk, which are your favorite bands?')]
        self.assertEqual([(shout.author.name, shout.body) for shout in self.event.shouts[:10]], shouts)
    
    def testEventRecentShout(self):
        shout = self.event.recent_shout
        self.assertEqual((shout.author.name, shout.body),
                         ('Aeromaniac21280',
                          'It was a brillian show still jealous at some ppl who could meet them  video of joe perry banging the guitar in youtube, in between u will see a devils hand with the thorny black heavy metal wrist band, that hand IS MINE LOL!!!'))
        
apikey = "152a230561e72192b8b0f3e42362c6ff"        
api = Api(apikey, no_cache = True)

data = {
    'id': 216156,
    'title': 'Aerosmith',
    'description': 'Tickets priced at 1,800 and 1,200.',
    'image': {'large': 'http://userserve-ak.last.fm/serve/126/300793.jpg',
             'medium': 'http://userserve-ak.last.fm/serve/64/300793.jpg',
             'small': 'http://userserve-ak.last.fm/serve/34/300793.jpg'},
    'tag': 'lastfm:event=216156',
    'url': 'http://www.last.fm/event/216156'
}
    
for k,v in data.iteritems():
    def testFunc(self):
        self.assertEqual(getattr(self.event, k), v)
    setattr(TestEvent, "testEvent%s" % k.replace('_', ' ').title().replace(' ', ''), testFunc)          

test_suite = unittest.TestLoader().loadTestsFromTestCase(TestEvent)

if __name__ == '__main__':
    unittest.main()
