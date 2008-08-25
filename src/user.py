#!/usr/bin/env python

__author__ = "Abhinav Sarkar <abhinav@abhinavsarkar.net>"
__version__ = "0.1"
__license__ = "GNU Lesser General Public License"

from base import LastfmBase

class User(LastfmBase):
    """A class representing an user."""
    def init(self,
                 api,
                 name = None,
                 url = None,
                 image = None,
                 stats = None):
        if not isinstance(api, Api):
            raise LastfmError("api reference must be supplied as an argument")
        self.__api = api
        self.__name = name
        self.__url = url
        self.__image = image
        self.__stats = stats and Stats(
                             subject = self,
                             match = stats.match,
                             weight = stats.weight
                            )
        self.__events = None
        self.__pastEvents = None
        self.__friends = None
        self.__neighbours = None
        self.__lovedTracks = None
        self.__topAlbums = None
        self.__topArtists = None
        self.__topTracks = None
        self.__topTags = None
        self.__lirary = User.Library(api, self)

    @property
    def name(self):
        """name of the user"""
        return self.__name

    @property
    def url(self):
        """url of the user's page"""
        return self.__url

    @property
    def image(self):
        """image of the user"""
        return self.__image

    @property
    def stats(self):
        """stats for the user"""
        return self.__stats

    @property
    def events(self):
        if self.__events is None:
            params = {'method': 'user.getevents', 'user': self.name}
            data = self.__api._fetchData(params).find('events')

            self.__events = [
                Event.createFromData(self.__api, e)
                for e in data.findall('event')
                ]
        return self.__events

    def getPastEvents(self,
                      page = None,
                      limit = None):
        params = {'method': 'user.getpastevents', 'user': self.name}
        if page is not None:
            params.update({'page': page})
        if limit is not None:
            params.update({'limit': limit})
    
        data = self.__api._fetchData(params).find('events')
        return [
            Event.createFromData(self.__api, e)
            for e in data.findall('event')
            ]
        
    @property
    def pastEvents(self):
        if self.__pastEvents is None:
            self.__pastEvents = self.getPastEvents()
        return self.__pastEvents

    def getFriends(self,
                   limit = None):
        params = {'method': 'user.getfriends', 'user': self.name}
        if limit is not None:
            params.update({'limit': limit})
        data = self.__api._fetchData(params).find('friends')
        return [
            User(
                self.__api,
                name = u.findtext('name'),
                image = dict([(i.get('size'), i.text) for i in u.findall('image')]),
                url = u.findtext('url'),
            )
            for u in data.findall('user')
        ]


    @property
    def friends(self):
        """friends of the user"""
        if self.__friends is None:
            self.__friends = self.getFriends()
        return self.__friends

    def getNeighbours(self, limit = None):
        params = {'method': 'user.getneighbours', 'user': self.name}
        if limit is not None:
            params.update({'limit': limit})
        data = self.__api._fetchData(params).find('neighbours')
        return [
                User(
                    self.__api,
                    name = u.findtext('name'),
                    image = {'medium': u.findtext('image')},
                    url = u.findtext('url'),
                    stats = Stats(
                                  subject = u.findtext('name'),
                                  match = float(u.findtext('match')),
                                  ),
                )
                for u in data.findall('user')
            ]

    @property
    def neighbours(self):
        """neighbours of the user"""
        if self.__neighbours is None:
            self.__neighbours = self.getNeighbours()
        return self.__neighbours
    
    @LastfmBase.topProperty("neighbours")
    def nearestNeighbour(self):
        """nearest neightbour of the user"""
        pass
    
    @property
    def playlists(self):
        """playlists of the user"""
        pass

    @property
    def lovedTracks(self):
        if self.__lovedTracks is None:
            params = {'method': 'user.getlovedtracks', 'user': self.name}
            data = self.__api._fetchData(params).find('lovedtracks')
            self.__lovedTracks = [
                    Track(
                        self.__api,
                        name = t.findtext('name'),
                        artist = Artist(
                            self.__api,
                            name = t.findtext('artist/name'),
                            mbid = t.findtext('artist/mbid'),
                            url = t.findtext('artist/url'),
                        ),
                        mbid = t.findtext('mbid'),
                        image = dict([(i.get('size'), i.text) for i in t.findall('image')]),
                        lovedOn = datetime(*(
                            time.strptime(
                                t.findtext('date').strip(),
                                '%d %b %Y, %H:%M'
                                )[0:6])
                            )
                        )
                    for t in data.findall('track')
                    ]
        return self.__lovedTracks

    def getRecentTracks(self, limit = None):
        params = {'method': 'user.getrecenttracks', 'user': self.name}
        data = self.__api._fetchData(params, no_cache = True).find('recenttracks')
        return [
                Track(
                      self.__api,
                      name = t.findtext('name'),
                      artist = Artist(
                                      self.__api,
                                      name = t.findtext('artist'),
                                      mbid = t.find('artist').attrib['mbid'],
                                      ),
                      album = Album(
                                    self.__api,
                                    name = t.findtext('album'),
                                    artist = Artist(
                                                    self.__api,
                                                    name = t.findtext('artist'),
                                                    mbid = t.find('artist').attrib['mbid'],
                                                    ),
                                    mbid = t.find('album').attrib['mbid'],
                                    ),
                      mbid = t.findtext('mbid'),
                      streamable = (t.findtext('streamable') == '1'),
                      url = t.findtext('url'),
                      image = dict([(i.get('size'), i.text) for i in t.findall('image')]),
                      playedOn = datetime(*(
                                           time.strptime(
                                                         t.findtext('date').strip(),
                                                         '%d %b %Y, %H:%M'
                                                         )[0:6])
                                           )
                      )
                      for t in data.findall('track')
                      ]

    @property
    def recentTracks(self):
        """recent tracks played by the user"""
        return self.getRecentTracks()

    @LastfmBase.topProperty("recentTracks")
    def mostRecentTrack(self):
        """most recent track played by the user"""
        pass

    def getTopAlbums(self, period = None):
        params = {'method': 'user.gettopalbums', 'user': self.name}
        if period is not None:
            params.update({'period': period})
        data = self.__api._fetchData(params).find('topalbums')

        return [
                Album(
                     self.__api,
                     name = a.findtext('name'),
                     artist = Artist(
                                     self.__api,
                                     name = a.findtext('artist/name'),
                                     mbid = a.findtext('artist/mbid'),
                                     url = a.findtext('artist/url'),
                                     ),
                     mbid = a.findtext('mbid'),
                     url = a.findtext('url'),
                     image = dict([(i.get('size'), i.text) for i in a.findall('image')]),
                     stats = Stats(
                                   subject = a.findtext('name'),
                                   playcount = int(a.findtext('playcount')),
                                   rank = int(a.attrib['rank'])
                                   )
                     )
                for a in data.findall('album')
                ]

    @property
    def topAlbums(self):
        """overall top albums of the user"""
        if self.__topAlbums is None:
            self.__topAlbums = self.getTopAlbums()
        return self.__topAlbums
    
    @LastfmBase.topProperty("topAlbums")
    def topAlbum(self):
        """overall top most album of the user"""
        pass

    def getTopArtists(self, period = None):
        params = {'method': 'user.gettopartists', 'user': self.name}
        if period is not None:
            params.update({'period': period})
        data = self.__api._fetchData(params).find('topartists')
        
        return [
                Artist(
                       self.__api,
                       name = a.findtext('name'),
                       mbid = a.findtext('mbid'),
                       stats = Stats(
                                     subject = a.findtext('name'),
                                     rank = a.attrib['rank'].strip() and int(a.attrib['rank']) or None,
                                     playcount = a.findtext('playcount') and int(a.findtext('playcount')) or None
                                     ),
                       url = a.findtext('url'),
                       streamable = (a.findtext('streamable') == "1"),
                       image = dict([(i.get('size'), i.text) for i in a.findall('image')]),
                       )
                for a in data.findall('artist')
                ]

    @property
    def topArtists(self):
        """top artists of the user"""
        if self.__topArtists is None:
            self.__topArtists = self.getTopArtists()
        return self.__topArtists

    @LastfmBase.topProperty("topArtists")
    def topArtist(self):
        """top artist of the user"""
        pass

    def getTopTracks(self, period = None):
        params = {'method': 'user.gettoptracks', 'user': self.name}
        if period is not None:
            params.update({'period': period})
        data = self.__api._fetchData(params).find('toptracks')
        return [
                Track(
                      self.__api,
                      name = t.findtext('name'),
                      artist = Artist(
                                      self.__api,
                                      name = t.findtext('artist/name'),
                                      mbid = t.findtext('artist/mbid'),
                                      url = t.findtext('artist/url'),
                                      ),
                      mbid = t.findtext('mbid'),
                      stats = Stats(
                                    subject = t.findtext('name'),
                                    rank = t.attrib['rank'].strip() and int(t.attrib['rank']) or None,
                                    playcount = t.findtext('playcount') and int(t.findtext('playcount')) or None
                                    ),
                      streamable = (t.findtext('streamable') == '1'),
                      fullTrack = (t.find('streamable').attrib['fulltrack'] == '1'),
                      image = dict([(i.get('size'), i.text) for i in t.findall('image')]),
                      )
                for t in data.findall('track')
                ]

    @property
    def topTracks(self):
        """top tracks of the user"""
        if self.__topTracks is None:
            self.__topTracks = self.getTopTracks()
        return self.__topTracks

    @LastfmBase.topProperty("topTracks")
    def topTrack(self):
        """top track of the user"""
        return (len(self.topTracks) and self.topTracks[0] or None)

    def getTopTags(self, limit = None):
        params = {'method': 'user.gettoptags', 'user': self.name}
        if limit is not None:
            params.update({'limit': limit})
        data = self.__api._fetchData(params).find('toptags')
        return [
                Tag(
                    self.__api,
                    name = t.findtext('name'),
                    url = t.findtext('url'),
                    stats = Stats(
                                  subject = t.findtext('name'),
                                  count = int(t.findtext('count'))
                                  )
                    ) 
                for t in data.findall('tag')
                ]

    @property
    def topTags(self):
        """top tags of the user"""
        if self.__topTags is None:
            self.__topTags = self.getTopTags()
        return self.__topTags

    @LastfmBase.topProperty("topTags")
    def topTag(self):
        """top tag of the user"""
        pass

    @property
    def weeklyChartList(self):
        pass

    def getWeeklyAlbumChart(self,
                             start = None,
                             end = None):
        pass

    @property
    def recentWeeklyAlbumChart(self):
        return self.getWeeklyAlbumChart()

    def getWeeklyArtistChart(self,
                             start = None,
                             end = None):
        pass

    @property
    def recentWeeklyArtistChart(self):
        return self.getWeeklyArtistChart()

    def getWeeklyTrackChart(self,
                             start = None,
                             end = None):
        pass

    @property
    def recentWeeklyTrackChart(self):
        return self.getWeeklyTrackChart()
    
    @property
    def library(self):
        return self.__lirary

    @staticmethod
    def hashFunc(*args, **kwds):
        try:
            return hash(kwds['name'])
        except KeyError:
            raise LastfmError("name has to be provided for hashing")

    def __hash__(self):
        return self.__class__.hashFunc(name = self.name)

    def __eq__(self, other):
        return self.name == other.name

    def __lt__(self, other):
        return self.name < other.name

    def __repr__(self):
        return "<lastfm.User: %s>" % self.name
    
    class Library(object):
        def __init__(self, api, user):
            self.__api = api
            self.__user = user
            self.__albums = None
            self.__artists = None
            self.__tracks = None
            
        @property
        def user(self):
            return self.__user
            
        def getAlbums(self,
                      limit = None,
                      page = None):
            params = {'method': 'library.getalbums'}
            data = self._fetchData(params, limit, page).find('albums')
            return {
                    'page': int(data.attrib['page']),
                    'perPage': int(data.attrib['perPage']),
                    'totalPages': int(data.attrib['totalPages']),
                    'albums': [
                               Album(
                                     self.__api,
                                     name = a.findtext('name'),
                                     artist = Artist(
                                                     self.__api,
                                                     name = a.findtext('artist/name'),
                                                     mbid = a.findtext('artist/mbid'),
                                                     url = a.findtext('artist/url'),
                                                     ),
                                     mbid = a.findtext('mbid'),
                                     url = a.findtext('url'),
                                     image = dict([(i.get('size'), i.text) for i in a.findall('image')]),
                                     stats = Stats(
                                                   subject = a.findtext('name'),
                                                   playcount = int(a.findtext('playcount')),
                                                   )
                                     )
                               for a in data.findall('album')
                               ]
                    }
            
        @property
        def albums(self):
            if self.__albums is None:
                self.__albums = self.getAlbums()['albums']
            return self.__albums
        
        def getArtists(self,
                       limit = None,
                       page = None):
            params = {'method': 'library.getartists'}
            data = self._fetchData(params, limit, page).find('artists')
            return {
                    'page': int(data.attrib['page']),
                    'perPage': int(data.attrib['perPage']),
                    'totalPages': int(data.attrib['totalPages']),
                    'artists': [
                                Artist(
                                       self.__api,
                                       name = a.findtext('name'),
                                       mbid = a.findtext('mbid'),
                                       stats = Stats(
                                                     subject = a.findtext('name'),
                                                     playcount = a.findtext('playcount') and int(a.findtext('playcount')) or None,
                                                     tagcount = a.findtext('tagcount') and int(a.findtext('tagcount')) or None
                                                     ),
                                       url = a.findtext('url'),
                                       streamable = (a.findtext('streamable') == "1"),
                                       image = dict([(i.get('size'), i.text) for i in a.findall('image')]),
                                       )
                                for a in data.findall('artist')
                                ]
                    }
            
        @property
        def artists(self):
            if self.__artists is None:
                self.__artists = self.getArtists()['artists']
            return self.__artists
        
        def getTracks(self,
                      limit = None,
                      page = None):
            params = {'method': 'library.gettracks'}
            data = self._fetchData(params, limit, page).find('tracks')
            return {
                    'page': int(data.attrib['page']),
                    'perPage': int(data.attrib['perPage']),
                    'totalPages': int(data.attrib['totalPages']),
                    'tracks': [
                               Track(
                                     self.__api,
                                     name = t.findtext('name'),
                                     artist = Artist(
                                                     self.__api,
                                                     name = t.findtext('artist/name'),
                                                     mbid = t.findtext('artist/mbid'),
                                                     url = t.findtext('artist/url'),
                                                     ),
                                     mbid = t.findtext('mbid'),
                                     stats = Stats(
                                                   subject = t.findtext('name'),
                                                   playcount = t.findtext('playcount') and int(t.findtext('playcount')) or None,
                                                   tagcount = t.findtext('tagcount') and int(t.findtext('tagcount')) or None
                                                   ),
                                     streamable = (t.findtext('streamable') == '1'),
                                     fullTrack = (t.find('streamable').attrib['fulltrack'] == '1'),
                                     image = dict([(i.get('size'), i.text) for i in t.findall('image')]),
                                     )
                               for t in data.findall('track')
                               ]
                    }
        
        @property
        def tracks(self):
            if self.__tracks is None:
                self.__tracks = self.getTracks()['tracks']
            return self.__tracks
        
        def _fetchData(self, params, limit, page):
            params .update({'user': self.user.name})
            if limit is not None:
                params.update({'limit': limit})
            if page is not None:
                params.update({'page': page})
                
            return self.__api._fetchData(params)
        
        def __repr__(self):
            return "<lastfm.User.Library: for user '%s'>" % self.user.name

from datetime import datetime
import time

from api import Api
from artist import Artist
from album import Album
from error import LastfmError
from event import Event
from stats import Stats
from tag import Tag
from track import Track

#TODO
#extract self.__* property as decorator
#write depaginations
#write exceptions
