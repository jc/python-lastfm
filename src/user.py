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
                 stats = None,
                 mostRecentTrack = None):
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
        self.__lovedTracks = None
        self.__mostRecentTrack = mostRecentTrack

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

    @property
    def pastEvents(self):
        if self.__pastEvents is None:
            params = {'method': 'user.getpastevents', 'user': self.name}
            data = self.__api._fetchData(params).find('events')

            self.__pastEvents = [
                Event.createFromData(self.__api, e)
                for e in data.findall('event')
                ]
        return self.__pastEvents

    def getFriends(self,
                   recentTrack = False,
                   limit = None):
        params = {'method': 'user.getfriends', 'user': self.name}
        if recentTrack:
            params.update({'recenttracks': 'true'})
        if limit is not None:
            params.update({'limit': limit})
        data = self.__api._fetchData(params).find('friends')
        if recentTrack:
            return [
                User(
                    self.__api,
                    name = u.findtext('name'),
                    image = dict([(i.get('size'), i.text) for i in u.findall('image')]),
                    url = u.findtext('url'),
                    mostRecentTrack = Track(
                        self.__api,
                        name = u.findtext('recenttrack/name'),
                        mbid = u.findtext('recenttrack/mbid'),
                        url = u.findtext('recenttrack/url'),
                        artist = Artist(
                            self.__api,
                            name = u.findtext('recenttrack/artist/name'),
                            mbid = u.findtext('recenttrack/artist/mbid'),
                            url = u.findtext('recenttrack/artist/url'),
                        ),
                    ),
                )
                for u in data.findall('user')
            ]
        else:
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
        pass

    @property
    def neighbours(self):
        """neightbours of the user"""
        return self.getNeighbours()

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
        pass

    @property
    def recentTracks(self):
        """recent tracks played by the user"""
        return self.getRecentTracks()

    @property
    def mostRecentTrack(self):
        """most recent track played by the user"""
        return (len(self.recentTracks) and self.recentTracks[0] or None)

    def getTopAlbums(self, period = None):
        pass

    @property
    def topAlbums(self):
        """top albums of the user"""
        return self.getTopAlbums()

    @property
    def topAlbum(self):
        """top album fo the user"""
        return (len(self.topAlbums) and self.topAlbums[0] or None)

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
from error import LastfmError
from event import Event
from stats import Stats
from track import Track
