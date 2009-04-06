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

class TestUser(unittest.TestCase):
    """ A test class for the Geo module. """
    def setUp(self):
        self.user = api.get_user('RJ')
        
    def tearDown(self):
        pass
    
    def testUserStats(self):
        self.assertAlmostEqual(self.user.nearest_neighbour.stats.match, 0.000826, 5)
        
    def testUserPastEvents(self):
        self.assertEqual([e.id for e in self.user.past_events[:5]],
                         [755511, 879065, 842991, 457062, 394026])
        
    def testUserFriends(self):
        friends = ['lobsterclaw', 'jajo', 'mremond', 'Orlenay', 'schlagschnitzel',
                  'Edouard', 'naniel', 'dunk', 'RUPERT', 'mxcl']
        self.assertEqual([f.name for f in self.user.friends[:10]], friends)
        
    def testUserNeighbours(self):
        neighbours = ['Lucas-Lentini', 'rockerD82', 'count-bassy', 'greg_a',
                      'STLJA', 'clauaud', 'Biaxident_', 'frood73', 'fillito',
                      'CHBeat']
        self.assertEqual([n.name for n in self.user.neighbours[:10]],
                         neighbours)
        
    def testUserNearestNeighbour(self):
        self.assertEqual(self.user.nearest_neighbour.name, 'Lucas-Lentini')
        
    def testUserPlaylists(self):
        self.assertEqual([p.id for p in self.user.playlists],
                         [5606, 2615079, 2614993, 2612216])
        
    def testUserLovedTracks(self):
        tracks = [('Young', 'Mokele'),
                 ('Hell March', 'Frank Klepacki'),
                 ('Summertime', 'Will Smith'),
                 ('Calm', 'Wayne Shorter'),
                 ('The One and Only', 'Chesney Hawkes'),
                 ('Cliffs of Dover', 'Eric Johnson'),
                 ('Orion (Instrumental)', 'Metallica'),
                 ('Whiskey in the Jar', 'Metallica'),
                 ('Loverman', 'Metallica'),
                 ('Turn the Page', 'Metallica')]
        self.assertEqual([(t.name, t.artist.name) for t in self.user.loved_tracks[:10]],
                         tracks)
        
    def testUserRecentTracks(self):
        tracks = [('Sahara', 'Cutting Crew'),
                 ("Don't Look Back", 'Cutting Crew'),
                 ('(I Just) Died in Your Arms', 'Cutting Crew'),
                 ('Fear of Falling', 'Cutting Crew'),
                 ('Life in a Dangerous Time', 'Cutting Crew'),
                 ("I've Been in Love Before", 'Cutting Crew'),
                 ('One for the Mockingbird', 'Cutting Crew'),
                 ('Any Colour', 'Cutting Crew'),
                 ('Brag', 'Cutting Crew'),
                 ('Binkies Return', 'Cutting Crew')]
        self.assertEqual([(t.name, t.artist.name) for t in self.user.recent_tracks[:10]],
                         tracks)
        
    def testUserMostRecentTrack(self):
        mrt = self.user.most_recent_track
        self.assertEquals((mrt.name, mrt.artist.name), ('Sahara', 'Cutting Crew'))
        
    def testUserTopAlbums(self):
        albums = [('Slave To The Grid', 'Skid Row'),
                 ('Images and Words', 'Dream Theater'),
                 ('Once in a Livetime', 'Dream Theater'),
                 ("Nina Simone's Finest Hour", 'Nina Simone'),
                 ('Sex and Religion', 'Steve Vai'),
                 ('title', "Slamin' Gladys"),
                 ('Time Bomb', 'Buckcherry'),
                 ('Day for Night', "Spock's Beard"),
                 ('Liquid Tension Experiment', 'Liquid Tension Experiment'),
                 ('Rage Against the Machine', 'Rage Against the Machine')]
        self.assertEqual([(a.name, a.artist.name) for a in self.user.top_albums[:10]],
                         albums)
        
    def testUserTopAlbum(self):
        ta = self.user.top_album
        self.assertEqual((ta.name, ta.artist.name), ('Slave To The Grid', 'Skid Row'))
        
    def testUserTopArtists(self):
        artists = ['Dream Theater', 'Dire Straits', 'Miles Davis', 'Metallica',
                   "Guns N' Roses", 'Aerosmith', 'Joe Satriani',
                   'Rage Against the Machine', 'Led Zeppelin', 'Buckcherry']
        self.assertEqual([a.name for a in self.user.top_artists[:10]],
                         artists)
        
    def testUserTopArtist(self):
        self.assertEqual(self.user.top_artist.name, 'Dream Theater')
        
    def testUserTopTracks(self):
        tracks = [('Learning to Live', 'Dream Theater'),
                 ('Three Minute Warning', 'Liquid Tension Experiment'),
                 ('Pull Me Under', 'Dream Theater'),
                 ('Take the Time', 'Dream Theater'),
                 ('Under a Glass Moon', 'Dream Theater'),
                 ('Another Day', 'Dream Theater'),
                 ('The Pusher', 'Steppenwolf'),
                 ('Sultans of Swing', 'Dire Straits'),
                 ('Wait for Sleep', 'Dream Theater'),
                 ('Caught in a Web', 'Dream Theater')]
        self.assertEqual( [(t.name, t.artist.name) for t in self.user.top_tracks[:10]],
                          tracks)
        
    def testUserTopTrack(self):
        tt = self.user.top_track
        self.assertEquals((tt.name, tt.artist.name),
                          ('Learning to Live', 'Dream Theater'))
        
    def testUserTopTags(self):
        tags = ['rock', 'jazz', 'metal', 'mellow', '80s',
                'guitar', 'checkitout', 'funky', 'stoner rock', 'funk']
        self.assertEquals([t.name for t in self.user.top_tags[:10]], tags)
        
    def testUserTopTag(self):
        self.assertEquals(self.user.top_tag.name, 'rock')
        
    def testUserWeeklyChartList(self):
        wcl = [('Sun, 13 Feb 2005', 'Sun, 20 Feb 2005'),
                 ('Sun, 20 Feb 2005', 'Sun, 27 Feb 2005'),
                 ('Sun, 27 Feb 2005', 'Sun, 06 Mar 2005'),
                 ('Sun, 13 Mar 2005', 'Sun, 20 Mar 2005'),
                 ('Sun, 20 Mar 2005', 'Sun, 27 Mar 2005'),
                 ('Sun, 27 Mar 2005', 'Sun, 03 Apr 2005'),
                 ('Sun, 03 Apr 2005', 'Sun, 10 Apr 2005'),
                 ('Sun, 10 Apr 2005', 'Sun, 17 Apr 2005'),
                 ('Sun, 17 Apr 2005', 'Sun, 24 Apr 2005'),
                 ('Sun, 01 May 2005', 'Sun, 08 May 2005')]
        self.assertEqual(
            [
                (
                    wc.start.date().strftime('%a, %d %b %Y'),
                    wc.end.date().strftime('%a, %d %b %Y')
                )
                for wc in self.user.weekly_chart_list[:10]
            ],
            wcl
            )
    
    def testUserGetWeeklyArtistChart(self):
        artists = ['Dream Theater', 'R.E.M.', 'Metallica', 'The Smashing Pumpkins',
                   'Counting Crows', 'Ludwig van Beethoven', 'Johann Sebastian Bach',
                   'Mr. Big', 'Muse', 'Bruce Springsteen']
        wc = self.user.weekly_chart_list[0]
        self.assertEqual(
            [artist.name
             for artist in self.user.get_weekly_artist_chart(wc.start, wc.end).artists[:10]],
            artists)
        
    def testUserGetWeeklyAlbumChart(self):
        albums = [('1962-1966: The Red Album', 'The Beatles', 1),
                 ('The X List (Disc 2)', 'Placebo', 1),
                 ('Killing Ground', 'Saxon', 1),
                 ('Thriller', 'Michael Jackson', 1),
                 ('Deep Purple Hit The Road - Mk 2 & Mk 3', 'Deep Purple', 1),
                 ('Youth and Young Manhood', 'Kings of Leon', 1),
                 ('The Greyest of Blue Skies', 'Finger Eleven', 1),
                 ('Ultra', 'Depeche Mode', 1),
                 ('Sing the Sorrow', 'AFI', 1),
                 ('Reckless', 'Bryan Adams', 1)]
        wc = self.user.weekly_chart_list[0]
        self.assertEqual(
             [(album.name, album.artist.name, album.stats.playcount)
                for album 
                in self.user.get_weekly_album_chart(wc.start, wc.end).albums[:10]],
            albums)
        
    def testUserGetWeeklyTrackChart(self):
        tracks = [('This Is Love', 'PJ Harvey', 2),
                 ('Track 06', 'Muse', 1),
                 ('Snail', 'The Smashing Pumpkins', 1),
                 ('The Struggle Within', 'Metallica', 1),
                 ('Burn', 'Deep Purple', 1),
                 ('Loaded', 'Deacon Blue', 1),
                 ('Anything Goes', 'Frank Sinatra', 1),
                 ('Flying Home', 'Stanley Jordan', 1),
                 ('Blackmail', 'John Lee Hooker & Miles Davis', 1),
                 ("Ladie's Nite In Buffalo-", 'David Lee Roth', 1)]
        wc = self.user.weekly_chart_list[0]
        self.assertEqual(
             [(track.name, track.artist.name, track.stats.playcount)
                for track 
                in self.user.get_weekly_track_chart(wc.start, wc.end).tracks[:10]],
            tracks)
        
    def testUserGetWeeklyTagChart(self):
        tags = [('rock', 134),
                ('alternative', 126),
                ('metal', 97),
                ('alternative rock', 91), 
                ('hard rock', 71), 
                ('female vocalists', 62), 
                ('classic rock', 54), 
                ('jazz', 42), 
                ('guitar virtuoso', 41), 
                ('baroque', 37)]
        wc = self.user.weekly_chart_list[0]
        self.assertEqual(
             [(tag.name, tag.stats.count)
                for tag
                in self.user.get_weekly_tag_chart(wc.start, wc.end).tags[:10]],
            tags)
        
    def testUserCompare(self):
        tm = self.user.compare('abhin4v')
        self.assertAlmostEqual(tm.score, 0.81405, 4)
        self.assertEqual([a.name for a in tm.artists],
            ['Coldplay', 'Red Hot Chili Peppers', 'The Killers', 'The Beatles', 'U2'])
        
    def testUserShouts(self):
        shouts = [('phillip360', 'Thu Mar  5 00:09:40 2009'),
                 ('newkid7', 'Tue Mar  3 05:09:25 2009'),
                 ('SZEKLER', 'Mon Mar  2 20:56:43 2009'),
                 ('JRoar', 'Sun Feb 22 16:25:41 2009'),
                 ('j0hnj0nes', 'Sat Feb 21 15:53:30 2009'),
                 ('Hloppering', 'Wed Feb 18 12:14:08 2009'),
                 ('Aramaki_', 'Mon Feb 16 19:01:13 2009'),
                 ('ANTIQCOOL', 'Sat Feb  7 04:07:33 2009'),
                 ('da-sha-sha', 'Wed Feb  4 22:21:36 2009'),
                 ('HaTeNL', 'Sun Feb  1 13:42:43 2009')]
        self.assertEqual([(shout.author.name, shout.date.ctime()) for shout
                          in self.user.shouts[:10]], shouts)
    
    def testUserRecentShout(self):
        shout = self.user.recent_shout
        self.assertEqual((shout.author.name, shout.date.ctime()),
                         ('phillip360', 'Thu Mar  5 00:09:40 2009'))
        
    def testUserLibraryAlbums(self):
        albums = [('Dire Straits', 'Dire Straits', 126),
                 ('The History of Rock', 'Kid Rock', 125),
                 ('Awake', 'Dream Theater', 124),
                 ('And All That Could Have Been', 'Nine Inch Nails', 124),
                 ('A Night at the Hip Hopera', 'The Kleptones', 124),
                 ('Doggystyle', 'Snoop Dogg', 124),
                 ('Evergreen', 'Echo & the Bunnymen', 122),
                 ('Falling Into Infinity', 'Dream Theater', 121),
                 ('Blood Sugar Sex Magik', 'Red Hot Chili Peppers', 117),
                 ('The Very Best of Level 42', 'Level 42', 116)]
        self.assertEqual([(album.name, album.artist.name, album.stats.playcount)
                          for album in self.user.library.albums[10:20]], albums)
        
    def testUserLibraryArtists(self):
        artists = ['Mr. Big', 'Jimi Hendrix', 'Nine Inch Nails',
                   'Nina Simone', 'Red Hot Chili Peppers', 'Snoop Dogg',
                   'Counting Crows', 'Def Leppard', 'Firebird', 'Free']
        self.assertEqual([artist.name for artist
                          in self.user.library.artists[10:20]], artists)
        
    def testUserLibraryTracks(self):
        tracks = [('All Right Now', 'Free', 30),
                 ('Surfing With the Alien', 'Joe Satriani', 30),
                 ('Cowboys', 'Portishead', 29),
                 ('Trial of Tears', 'Dream Theater', 29),
                 ('All Along the Watchtower', 'Jimi Hendrix', 28),
                 ('Surrounded', 'Dream Theater', 28),
                 ('Closer', 'Nine Inch Nails', 28),
                 ('The Glass Prison', 'Dream Theater', 28),
                 ('Superstition', 'Stevie Wonder', 28),
                 ('Hollow Years', 'Dream Theater', 28)]
        self.assertEqual([(track.name, track.artist.name, track.stats.playcount)
                          for track in self.user.library.tracks[10:20]], tracks)
    
apikey = "152a230561e72192b8b0f3e42362c6ff"        
api = Api(apikey, no_cache = True)
        
data = {
    'name': 'RJ',
    'real_name': 'Richard Jones ',
    'url': 'http://www.last.fm/user/RJ',
    'image': {'large': 'http://userserve-ak.last.fm/serve/126/8270359.jpg',
                 'medium': 'http://userserve-ak.last.fm/serve/64/8270359.jpg',
                 'small': 'http://userserve-ak.last.fm/serve/34/8270359.jpg'},
    'autheticated': False,
    'events': [api.get_event(834368)]
}
for k,v in data.iteritems():
    def testFunc(self):
        self.assertEqual(getattr(self.user, k), v)
    setattr(TestUser, "testUser%s" % k.replace('_', ' ').title().replace(' ', ''), testFunc)
                
test_suite = unittest.TestLoader().loadTestsFromTestCase(TestUser)

if __name__ == '__main__':
    unittest.main()
