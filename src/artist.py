#!/usr/bin/env python

__author__ = "Abhinav Sarkar"
__version__ = "0.1"
__license__ = "GNU Lesser General Public License"

from base import LastfmBase

class Artist(LastfmBase):
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
            raise LastfmError("api reference must be supplied as an argument")
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
        self.__bio = bio and Bio(
                         artist = self,
                         published = bio.published,
                         summary = bio.summary,
                         content = bio.content
                        )
        self.__events = None
        self.__topAlbums = None
        self.__topTracks = None
        self.__topFans = None

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

    def getSimilar(self, limit = None):
        params = {
                  'method': 'artist.getsimilar',
                  'artist': self.__name
                  }
        if limit is not None:
            params.update({'limit': limit})
        data = self.__api._fetchData(params).find('similarartists')
        self.__similar = [
                          Artist(
                                 self.__api,
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
        return self.__similar

    @property
    def similar(self):
        """artists similar to this artist"""
        if self.__similar is None:
            return self.getSimilar()
        return self.__similar
    
    @property
    def mostSimilar(self):
        """artist most similar to this artist"""
        return (len(self.similar) and self.similar[0] or None)
    
    @property
    def topTags(self):
        """top tags for the artist"""
        if self.__topTags is None or len(self.__topTags) < 6:
            params = {
                      'method': 'artist.gettoptags',
                      'artist': self.__name
                      }
            data = self.__api._fetchData(params).find('toptags')
            self.__topTags = [
                              Tag(
                                  self.__api,
                                  name = t.findtext('name'),
                                  url = t.findtext('url')
                                  )
                              for t in data.findall('tag')
                              ]
        return self.__topTags
    
    @property
    def topTag(self):
        """top tag for the artist"""
        return (len(self.topTags) and self.topTags[0] or None)

    @property
    def bio(self):
        """biography of the artist"""
        if self.__bio is None:
            self._fillInfo()
        return self.__bio
    
    @property
    def events(self):
        """events for the artist"""
        if self.__events is None:
            params = {'method': 'artist.getevents', 'artist': self.name}
            data = self.__api._fetchData(params).find('events')
            
            self.__events = [
                    Event(
                          self.__api,
                          id = int(e.findtext('id')),
                          title = e.findtext('title'),
                          artists = [Artist(self.__api, name = a.text) for a in e.findall('artists/artist')],
                          headliner = Artist(self.__api, name = e.findtext('artists/headliner')),
                          venue = Venue(
                                        name = e.findtext('venue/name'),
                                        location = Location(
                                                            self.__api,
                                                            city = e.findtext('venue/location/city'),
                                                            country = Country(
                                                                self.__api,
                                                                name = e.findtext('venue/location/country')
                                                                ),
                                                            street = e.findtext('venue/location/street'),
                                                            postalCode = e.findtext('venue/location/postalcode'),
                                                            latitude = float(e.findtext(
                                                                'venue/location/{%s}point/{%s}lat' % ((Location.xmlns,)*2)
                                                                )),
                                                            longitude = float(e.findtext(
                                                                'venue/location/{%s}point/{%s}long' % ((Location.xmlns,)*2)
                                                                )),
                                                            timezone = e.findtext('venue/location/timezone')
                                                            ),
                                        url = e.findtext('venue/url')
                                        ),
                          startDate = e.findtext('startDate') and 
                                        datetime(*(time.strptime(e.findtext('startDate').strip(), '%a, %d %b %Y')[0:6])) or
                                        None,
                          startTime = e.findtext('startTime') and 
                                        datetime(*(time.strptime(e.findtext('startTime').strip(), '%H:%M')[0:6])) or
                                        None,
                          description = e.findtext('description'),
                          image = dict([(i.get('size'), i.text) for i in e.findall('image')]),
                          url = e.findtext('url')
                          )
                    for e in data.findall('event')
                    ]
        return self.__events
    
    @property
    def topAlbums(self):
        """top albums of the artist"""
        if self.__topAlbums is None:
            params = {'method': 'artist.gettopalbums', 'artist': self.name}
            data = self.__api._fetchData(params).find('topalbums')
            
            self.__topAlbums = [
                    Album(
                         self.__api,
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
        return self.__topAlbums
        
    @property
    def topAlbum(self):
        """top album of the artist"""
        return (len(self.topAlbums) and self.topAlbums[0] or None)
    
    @property
    def topFans(self):
        """top fans of the artist"""
        if self.__topFans is None:
            params = {'method': 'artist.gettopfans', 'artist': self.name}
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
        """top fan of the artist"""
        return (len(self.topFans) and self.topFans[0] or None)
    
    @property
    def topTracks(self):
        """top tracks of the artist"""
        if self.__topTracks is None:
            params = {'method': 'artist.gettoptracks', 'artist': self.name}
            data = self.__api._fetchData(params).find('toptracks')
            self.__topTracks = [
                    Track(
                          self.__api,
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
        return self.__topTracks
    
    @property
    def topTrack(self):
        return (len(self.topTracks) and self.topTracks[0] or None)
    
    @staticmethod
    def search(api,
               artist,
               limit = None,
               page = None):
        params = {'method': 'artist.search', 'artist': artist}
        if limit:
            params.update({'limit': limit})
        if page:
            params.update({'page': page})
        data = api._fetchData(params).find('results')
        return SearchResult(
                            type = 'artist',
                            searchTerms = data.find("{%s}Query" % SearchResult.xmlns).attrib['searchTerms'],
                            startPage = int(data.find("{%s}Query" % SearchResult.xmlns).attrib['startPage']),
                            totalResults = int(data.findtext("{%s}totalResults" % SearchResult.xmlns)),
                            startIndex = int(data.findtext("{%s}startIndex" % SearchResult.xmlns)),
                            itemsPerPage = int(data.findtext("{%s}itemsPerPage" % SearchResult.xmlns)),
                            matches = [
                                       Artist(
                                              api,
                                              name = a.findtext('name'),
                                              mbid = a.findtext('mbid'),
                                              url = a.findtext('url'),
                                              image = dict([(i.get('size'), i.text) for i in a.findall('image')]),
                                              streamable = (a.findtext('streamable') == '1'),
                                              )
                                       for a in data.findall('artistmatches/artist')
                                       ]
                            )
        
    @staticmethod
    def _fetchData(api,
                artist = None,
                mbid = None):
        params = {'method': 'artist.getinfo'}
        if not (artist or mbid):
            raise LastfmError("either artist or mbid has to be given as argument.")
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
                                 name = a.findtext('name'),
                                 url = a.findtext('url'),
                                 image = dict([(i.get('size'), i.text) for i in a.findall('image')])
                                 )
                          for a in data.findall('similar/artist')
                          ]
        self.__topTags = [
                          Tag(
                              self.__api,
                              name = t.findtext('name'),
                              url = t.findtext('url')
                              ) 
                          for t in data.findall('tags/tag')
                          ]
        self.__bio = Bio(
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
        if a.bio is None:
            a._fillInfo()
        return a
                
    @staticmethod
    def hashFunc(*args, **kwds):
        try:
            return hash(kwds['name'].lower())
        except KeyError:
            try:
                print args[1].lower()
                return hash(args[1].lower())
            except IndexError:
                raise LastfmError("name has to be provided for hashing")
        
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

class Bio(object):
    """A class representing the biography of an artist."""
    def __init__(self,
                 artist,
                 published = None,
                 summary = None,
                 content = None):
        self.__artist = artist
        self.__published = published
        self.__summary = summary
        self.__content = content

    @property
    def artist(self):
        """artist for which the biography is"""
        return self.__artist

    @property
    def published(self):
        """publication time of the biography"""
        return self.__published

    @property
    def summary(self):
        """summary of the biography"""
        return self.__summary

    @property
    def content(self):
        """content of the biography"""
        return self.__content

    def __repr__(self):
        return "<lastfm.artist.Bio: for artist '%s'>" % self.__artist.name

from datetime import datetime
import time

from api import Api
from album import Album
from error import LastfmError
from event import Event
from geo import Country, Location, Venue
from tag import Tag
from track import Track
from user import User
from search import SearchResult
from stats import Stats