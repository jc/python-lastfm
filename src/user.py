#!/usr/bin/env python

__author__ = "Abhinav Sarkar"
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
        pass

    @property
    def topArtists(self):
        """top artists of the user"""
        return self.getTopArtists()

    @property
    def topArtist(self):
        """top artist of the user"""
        return (len(self.topArtists) and self.topArtists[0] or None)

    def getTopTracks(self, period = None):
        pass

    @property
    def topTracks(self):
        """top tracks of the user"""
        return self.getTopTracks()

    @property
    def topTrack(self):
        """top track of the user"""
        return (len(self.topTracks) and self.topTracks[0] or None)

    def getTopTags(self, limit = None):
        pass

    @property
    def topTags(self):
        """top tags of the user"""
        return self.getTopTags()

    @property
    def topTag(self):
        """top tag of the user"""
        return (len(self.topTags) and self.topTags[0] or None)

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

from datetime import datetime
import time

from api import Api
from artist import Artist
from album import Album
from error import LastfmError
from event import Event
from stats import Stats
from track import Track
