#!/usr/bin/env python

__author__ = "Abhinav Sarkar <abhinav@abhinavsarkar.net>"
__version__ = "0.2"
__license__ = "GNU Lesser General Public License"

from base import LastfmBase
from taggable import Taggable
from lazylist import lazylist

class Artist(Taggable, LastfmBase):
    """A class representing an artist."""
    def init(self,
                 api,
                 name = None,
                 mbid = None,
                 url = None,
                 image = None,
                 streamable = None,
                 stats = None,
                 similar = None,
                 topTags = None,
                 bio = None):
        if not isinstance(api, Api):
            raise LastfmInvalidParametersError("api reference must be supplied as an argument")
        super(self.__class__, self).init(api)
        self.__api = api
        self.__name = name
        self.__mbid = mbid
        self.__url = url
        self.__image = image
        self.__streamable = streamable
        self.__stats = stats and Stats(
                             subject = self,
                             listeners = stats.listeners,
                             playcount = stats.playcount,
                             match = stats.match,
                             rank = stats.rank
                            )
        self.__similar = similar
        self.__topTags = topTags
        self.__bio = bio and Wiki(
                         subject = self,
                         published = bio.published,
                         summary = bio.summary,
                         content = bio.content
                        )

    @property
    def name(self):
        """name of the artist"""
        return self.__name

    @property
    def mbid(self):
        """mbid of the artist"""
        if self.__mbid is None:
            self._fillInfo()
        return self.__mbid

    @property
    def url(self):
        """url of the artist's page"""
        if self.__url is None:
            self._fillInfo()
        return self.__url

    @property
    def image(self):
        """images of the artist"""
        if self.__image is None:
            self._fillInfo()
        return self.__image

    @property
    def streamable(self):
        """is the artist streamable"""
        if self.__streamable is None:
            self._fillInfo()
        return self.__streamable

    @property
    def stats(self):
        """stats for the artist"""
        if self.__stats is None:
            self._fillInfo()
        return self.__stats

    def _defaultParams(self, extraParams = None):
        if not self.name:
            raise LastfmInvalidParametersError("artist has to be provided.")
        params = {'artist': self.name}
        if extraParams is not None:
            params.update(extraParams)
        return params
    
    def getSimilar(self, limit = None):
        params = self._defaultParams({'method': 'artist.getSimilar'})
        if limit is not None:
            params.update({'limit': limit})
        data = self.__api._fetchData(params).find('similarartists')
        self.__similar = [
                          Artist(
                                 self.__api,
                                 subject = self,
                                 name = a.findtext('name'),
                                 mbid = a.findtext('mbid'),
                                 stats = Stats(
                                               subject = a.findtext('name'),
                                               match = float(a.findtext('match')),
                                               ),
                                 url = 'http://' + a.findtext('url'),
                                 image = {'large': a.findtext('image')}
                                 )
                          for a in data.findall('artist')
                          ]
        return self.__similar[:]

    @property
    def similar(self):
        """artists similar to this artist"""
        if self.__similar is None or len(self.__similar) < 6:
            return self.getSimilar()
        return self.__similar[:]

    @LastfmBase.topProperty("similar")
    def mostSimilar(self):
        """artist most similar to this artist"""
        pass

    @property
    def topTags(self):
        """top tags for the artist"""
        if self.__topTags is None or len(self.__topTags) < 6:
            params = self._defaultParams({'method': 'artist.getTopTags'})
            data = self.__api._fetchData(params).find('toptags')
            self.__topTags = [
                              Tag(
                                  self.__api,
                                  subject = self,
                                  name = t.findtext('name'),
                                  url = t.findtext('url')
                                  )
                              for t in data.findall('tag')
                              ]
        return self.__topTags[:]

    @LastfmBase.topProperty("topTags")
    def topTag(self):
        """top tag for the artist"""
        pass

    @property
    def bio(self):
        """biography of the artist"""
        if self.__bio is None:
            self._fillInfo()
        return self.__bio

    @LastfmBase.cachedProperty
    def events(self):
        """events for the artist"""
        params = self._defaultParams({'method': 'artist.getEvents'})
        data = self.__api._fetchData(params).find('events')

        return [
                Event.createFromData(self.__api, e)
                for e in data.findall('event')
                ]

    @LastfmBase.cachedProperty
    def topAlbums(self):
        """top albums of the artist"""
        params = self._defaultParams({'method': 'artist.getTopAlbums'})
        data = self.__api._fetchData(params).find('topalbums')

        return [
                Album(
                     self.__api,
                     subject = self,
                     name = a.findtext('name'),
                     artist = self,
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

    @LastfmBase.topProperty("topAlbums")
    def topAlbum(self):
        """top album of the artist"""
        pass

    @LastfmBase.cachedProperty
    def topFans(self):
        """top fans of the artist"""
        params = self._defaultParams({'method': 'artist.getTopFans'})
        data = self.__api._fetchData(params).find('topfans')
        return [
                User(
                     self.__api,
                     subject = self,
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
    
    @LastfmBase.topProperty("topFans")
    def topFan(self):
        """top fan of the artist"""
        pass

    @LastfmBase.cachedProperty
    def topTracks(self):
        """top tracks of the artist"""
        params = self._defaultParams({'method': 'artist.getTopTracks'})
        data = self.__api._fetchData(params).find('toptracks')
        return [
                Track(
                      self.__api,
                      subject = self,
                      name = t.findtext('name'),
                      artist = self,
                      mbid = t.findtext('mbid'),
                      stats = Stats(
                                    subject = t.findtext('name'),
                                    playcount = int(t.findtext('playcount')),
                                    rank = int(t.attrib['rank'])
                                    ),
                      streamable = (t.findtext('streamable') == '1'),
                      fullTrack = (t.find('streamable').attrib['fulltrack'] == '1'),
                      image = dict([(i.get('size'), i.text) for i in t.findall('image')]),
                      )
                for t in data.findall('track')
                ]
    
    @LastfmBase.topProperty("topTracks")
    def topTrack(self):
        """topmost fan of the artist"""
        pass

    @staticmethod
    def search(api,
               artist,
               limit = None):
        params = {'method': 'artist.search', 'artist': artist}
        if limit:
            params.update({'limit': limit})
            
        @lazylist
        def gen(lst):
            data = api._fetchData(params).find('results')
            totalPages = int(data.findtext("{%s}totalResults" % Api.SEARCH_XMLNS))/ \
                            int(data.findtext("{%s}itemsPerPage" % Api.SEARCH_XMLNS)) + 1
            
            @lazylist
            def gen2(lst, data):
                for a in data.findall('artistmatches/artist'):
                    yield Artist(
                                 api,
                                 name = a.findtext('name'),
                                 mbid = a.findtext('mbid'),
                                 url = a.findtext('url'),
                                 image = dict([(i.get('size'), i.text) for i in a.findall('image')]),
                                 streamable = (a.findtext('streamable') == '1'),
                                 )
                          
            for a in gen2(data):
                yield a
            
            for page in xrange(2, totalPages+1):
                params.update({'page': page})
                data = api._fetchData(params).find('results')
                for a in gen2(data):
                    yield a
        return gen()
    
    @staticmethod
    def _fetchData(api,
                artist = None,
                mbid = None):
        params = {'method': 'artist.getInfo'}
        if not (artist or mbid):
            raise LastfmInvalidParametersError("either artist or mbid has to be given as argument.")
        if artist:
            params.update({'artist': artist})
        elif mbid:
            params.update({'mbid': mbid})
        return api._fetchData(params).find('artist')

    def _fillInfo(self):
        data = Artist._fetchData(self.__api, self.name)
        self.__name = data.findtext('name')
        self.__mbid = data.findtext('mbid')
        self.__url = data.findtext('url')
        self.__image = dict([(i.get('size'), i.text) for i in data.findall('image')])
        self.__streamable = (data.findtext('streamable') == 1)
        self.__stats = Stats(
                             subject = self,
                             listeners = int(data.findtext('stats/listeners')),
                             playcount = int(data.findtext('stats/playcount'))
                             )
        self.__similar = [
                          Artist(
                                 self.__api,
                                 subject = self,
                                 name = a.findtext('name'),
                                 url = a.findtext('url'),
                                 image = dict([(i.get('size'), i.text) for i in a.findall('image')])
                                 )
                          for a in data.findall('similar/artist')
                          ]
        self.__topTags = [
                          Tag(
                              self.__api,
                              subject = self,
                              name = t.findtext('name'),
                              url = t.findtext('url')
                              )
                          for t in data.findall('tags/tag')
                          ]
        self.__bio = Wiki(
                         self,
                         published = datetime(*(time.strptime(
                                                              data.findtext('bio/published').strip(),
                                                              '%a, %d %b %Y %H:%M:%S +0000'
                                                              )[0:6])),
                         summary = data.findtext('bio/summary'),
                         content = data.findtext('bio/content')
                         )

    @staticmethod
    def getInfo(api,
                artist = None,
                mbid = None):
        data = Artist._fetchData(api, artist, mbid)

        a = Artist(api, name = data.findtext('name'))
        a._fillInfo()
        return a

    @staticmethod
    def hashFunc(*args, **kwds):
        try:
            return hash(kwds['name'].lower())
        except KeyError:
            try:
                return hash(args[1].lower())
            except IndexError:
                raise LastfmInvalidParametersError("name has to be provided for hashing")

    def __hash__(self):
        return self.__class__.hashFunc(name = self.name)

    def __eq__(self, other):
        if self.mbid and other.mbid:
            return self.mbid == other.mbid
        if self.url and other.url:
            return self.url == other.url
        return self.name == other.name

    def __lt__(self, other):
        return self.name < other.name

    def __repr__(self):
        return "<lastfm.Artist: %s>" % self.__name

from datetime import datetime
import time

from album import Album
from api import Api
from error import LastfmInvalidParametersError
from event import Event
from stats import Stats
from tag import Tag
from track import Track
from user import User
from wiki import Wiki
