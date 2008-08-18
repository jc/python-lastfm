#!/usr/bin/env python

__author__ = "Abhinav Sarkar"
__version__ = "0.1"
__license__ = "GNU Lesser General Public License"

from base import LastfmBase

class Track(LastfmBase):
    """A class representing a track."""
    def init(self,
                 api,
                 name = None,
                 mbid = None,
                 url = None,
                 streamable = None,
                 artist = None,
                 image = None,
                 stats = None,
                 fullTrack = None):
        if not isinstance(api, Api):
            raise LastfmError("api reference must be supplied as an argument")
        self.__api = api
        self.__name = name
        self.__mbid = mbid
        self.__url = url
        self.__streamable = streamable
        self.__artist = artist
        self.__image = image
        self.__stats = stats and Stats(
                             subject = self,
                             match = stats.match,
                             playcount = stats.playcount,
                             rank = stats.rank,
                             listeners = stats.listeners,
                            )
        self.__fullTrack = fullTrack
        self.__similar = None
        self.__topFans = None
        self.__topTags = None

    @property
    def name(self):
        """name of the track"""
        return self.__name

    @property
    def mbid(self):
        """mbid of the track"""
        return self.__mbid

    @property
    def url(self):
        """url of the tracks's page"""
        return self.__url

    @property
    def streamable(self):
        """is the track streamable"""
        return self.__streamable

    @property
    def artist(self):
        """artist of the track"""
        return self.__artist

    @property
    def image(self):
        """image of the track's album cover"""
        return self.__image

    @property
    def stats(self):
        """stats of the track"""
        return self.__stats
    
    @property
    def fullTrack(self):
        """is the full track streamable"""
        return self.__fullTrack
    
    def __checkParams(self,
                      params,
                      artist = None,
                      track = None,
                      mbid = None):
        if not ((artist and track) or mbid):
            raise LastfmError("either (artist and track) or mbid has to be given as argument.")
        
        if artist and track:
            params.update({'artist': artist, 'track': track})
        elif mbid:
            params.update({'mbid': mbid})
        return params
        
    @property
    def similar(self):
        """tracks similar to this track"""
        if self.__similar is None:
            params = self.__checkParams(
                                        {'method': 'track.getsimilar'},
                                        self.artist.name,
                                        self.name,
                                        self.mbid
                                        )
            data = self.__api._fetchData(params).find('similartracks')
            self.__similar = [
                        Track(
                              self.__api,
                              name = t.findtext('name'),
                              artist = Artist(
                                              self.__api,
                                              name = t.findtext('artist/name'),
                                              mbid = t.findtext('artist/mbid'),
                                              url = t.findtext('artist/url')
                                              ),
                              mbid = t.findtext('mbid'),
                              stats = Stats(
                                            subject = t.findtext('name'),
                                            match = float(t.findtext('match'))
                                            ),
                              streamable = (t.findtext('streamable') == '1'),
                              fullTrack = (t.find('streamable').attrib['fulltrack'] == '1'),
                              image = dict([(i.get('size'), i.text) for i in t.findall('image')]),
                              )
                        for t in data.findall('track')
                        ]
        return self.__similar
    
    @property
    def mostSimilar(self):
        """track most similar to this track"""
        return (len(self.similar) and self.similar[0] or None)
        
    @property
    def topFans(self):
        """top fans of the track"""
        if self.__topFans is None:
            params = self.__checkParams(
                                        {'method': 'track.gettopfans'},
                                        self.artist.name,
                                        self.name,
                                        self.mbid
                                        )
            data = self.__api._fetchData(params).find('topfans')
            self.__topFans = [
                              User(
                                   self.__api,
                                   name = u.findtext('name'),
                                   url = u.findtext('url'),
                                   image = dict([(i.get('size'), i.text) for i in u.findall('image')]),
                                   stats = Stats(
                                                 subject = u.findtext('name'),
                                                 weight = int(u.findtext('weight'))
                                                 )
                                   )
                              for u in data.findall('user')
                              ]
        return self.__topFans
    
    @property
    def topFan(self):
        return (len(self.topFans) and self.topFans[0] or None)
        
    @property
    def topTags(self):
        """top tags for the track"""
        if self.__topTags is None:
            params = self.__checkParams(
                                        {'method': 'track.gettoptags'},
                                        self.artist.name,
                                        self.name,
                                        self.mbid
                                        )
            data = self.__api._fetchData(params).find('toptags')
            self.__topTags = [
                              Tag(
                                  self.__api,
                                  name = t.findtext('name'),
                                  url = t.findtext('url'),
                                  stats = Stats(
                                                subject = t.findtext('name'),
                                                count = int(t.findtext('count')),
                                                )
                                  )
                              for t in data.findall('tag')
                              ]
        return self.__topTags
    
    @property
    def topTag(self):
        return (len(self.topTags) and self.topTags[0] or None)
    
    @staticmethod
    def search(api,
               track,
               artist = None,
               limit = None,
               page = None):
        params = {'method': 'track.search', 'track': track}
        if artist is not None:
            params.update({'artist': artist})
        if limit is not None:
            params.update({'limit': limit})
        if page is not None:
            params.update({'page': page})
        data = api._fetchData(params).find('results')
        return SearchResult(
                            type = 'track',
                            searchTerms = data.find("{%s}Query" % SearchResult.xmlns).attrib['searchTerms'],
                            startPage = int(data.find("{%s}Query" % SearchResult.xmlns).attrib['startPage']),
                            totalResults = int(data.findtext("{%s}totalResults" % SearchResult.xmlns)),
                            startIndex = int(data.findtext("{%s}startIndex" % SearchResult.xmlns)),
                            itemsPerPage = int(data.findtext("{%s}itemsPerPage" % SearchResult.xmlns)),
                            matches = [
                                       Track(
                                              api,
                                              name = t.findtext('name'),
                                              artist = Artist(
                                                              api,
                                                              name = t.findtext('artist')
                                                              ),
                                              url = t.findtext('url'),
                                              stats = Stats(
                                                            subject = t.findtext('name'),
                                                            listeners = int(t.findtext('listeners'))
                                                            ),
                                              streamable = (t.findtext('streamable') == '1'),
                                              fullTrack = (t.find('streamable').attrib['fulltrack'] == '1'),
                                              image = dict([(i.get('size'), i.text) for i in t.findall('image')]),
                                              )
                                       for t in data.findall('trackmatches/track')
                                       ]
                            )
    
    @staticmethod
    def hashFunc(*args, **kwds):
        try:
            return hash("%s%s" % (kwds['name'], hash(kwds['artist'])))
        except KeyError:
            raise LastfmError("name and artist have to be provided for hashing")
        
    def __hash__(self):
        return self.__class__.hashFunc(name = self.name, artist = self.artist)
    
    def __eq__(self, other):
        if self.mbid and other.mbid:
            return self.mbid == other.mbid
        if self.url and other.url:
            return self.url == other.url
        if (self.name and self.artist) and (other.name and other.artist):
            return (self.name == other.name) and (self.artist == other.artist)
        return super(Track, self).__eq__(other)
    
    def __lt__(self, other):
        return self.name < other.name
    
    def __repr__(self):
        return "<lastfm.Track: '%s' by %s>" % (self.name, self.artist.name)

from api import Api
from artist import Artist
from error import LastfmError
from search import SearchResult
from stats import Stats
from tag import Tag
from user import User