#!/usr/bin/env python

__author__ = "Abhinav Sarkar <abhinav@abhinavsarkar.net>"
__version__ = "0.2"
__license__ = "GNU Lesser General Public License"

from base import LastfmBase
from lazylist import lazylist

class Tag(LastfmBase):
    """"A class representing a tag."""
    def init(self,
                 api,
                 name = None,
                 url = None,
                 streamable = None,
                 stats = None):
        if not isinstance(api, Api):
            raise LastfmInvalidParametersError("api reference must be supplied as an argument")
        self.__api = api
        self.__name = name
        self.__url = url
        self.__streamable = streamable
        self.__stats = stats and Stats(
                             subject = self,
                             count = stats.count
                             )
        
    @property
    def name(self):
        """name of the tag"""
        return self.__name

    @property
    def url(self):
        """url of the tag's page"""
        return self.__url
    
    @property
    def streamable(self):
        """is the tag streamable"""
        return self.__streamable
    
    @property
    def stats(self):
        return self.__stats
    
    @LastfmBase.cachedProperty
    def similar(self):
        """tags similar to this tag"""
        params = {'method': 'tag.getSimilar', 'tag': self.name}
        data = self.__api._fetchData(params).find('similartags')
        return [
                Tag(
                    self.__api,
                    subject = self,
                    name = t.findtext('name'),
                    url = t.findtext('url'),
                    streamable = (t.findtext('streamable') == "1"),
                    )
                for t in data.findall('tag')
                ]
    
    @LastfmBase.topProperty("similar")
    def mostSimilar(self):
        """most similar tag to this tag"""
        pass
    
    @LastfmBase.cachedProperty
    def topAlbums(self):
        """top albums for the tag"""
        params = {'method': 'tag.getTopAlbums', 'tag': self.name}
        data = self.__api._fetchData(params).find('topalbums')
        return [
                Album(
                      self.__api,
                      subject = self,
                      name = a.findtext('name'),
                      artist = Artist(
                                      self.__api,
                                      subject = self,
                                      name = a.findtext('artist/name'),
                                      mbid = a.findtext('artist/mbid'),
                                      url = a.findtext('artist/url'),
                                      ),
                      mbid = a.findtext('mbid'),
                      url = a.findtext('url'),
                      image = dict([(i.get('size'), i.text) for i in a.findall('image')]),
                      stats = Stats(
                                    subject = a.findtext('name'),
                                    tagcount = a.findtext('tagcount') and int(a.findtext('tagcount')) or None,
                                    rank = a.attrib['rank'].strip() and int(a.attrib['rank']) or None
                                    )
                      )
                for a in data.findall('album')
                ]

    @LastfmBase.topProperty("topAlbums")
    def topAlbum(self):
        """top album for the tag"""
        pass
    
    @LastfmBase.cachedProperty
    def topArtists(self):
        """top artists for the tag"""
        params = {'method': 'tag.getTopArtists', 'tag': self.name}
        data = self.__api._fetchData(params).find('topartists')
        return [
                Artist(
                       self.__api,
                       subject = self,
                       name = a.findtext('name'),
                       mbid = a.findtext('mbid'),
                       stats = Stats(
                                     subject = a.findtext('name'),
                                     rank = a.attrib['rank'].strip() and int(a.attrib['rank']) or None,
                                     tagcount = a.findtext('tagcount') and int(a.findtext('tagcount')) or None
                                     ),
                       url = a.findtext('url'),
                       streamable = (a.findtext('streamable') == "1"),
                       image = dict([(i.get('size'), i.text) for i in a.findall('image')]),
                       )
                for a in data.findall('artist')
                ]

    @LastfmBase.topProperty("topArtists")
    def topArtist(self):
        """top artist for the tag"""
        pass
    
    @LastfmBase.cachedProperty
    def topTracks(self):
        """top tracks for the tag"""
        params = {'method': 'tag.getTopTracks', 'tag': self.name}
        data = self.__api._fetchData(params).find('toptracks')
        return [
                Track(
                      self.__api,
                      subject = self,
                      name = t.findtext('name'),
                      artist = Artist(
                                      self.__api,
                                      subject = self,
                                      name = t.findtext('artist/name'),
                                      mbid = t.findtext('artist/mbid'),
                                      url = t.findtext('artist/url'),
                                      ),
                      mbid = t.findtext('mbid'),
                      stats = Stats(
                                    subject = t.findtext('name'),
                                    rank = t.attrib['rank'].strip() and int(t.attrib['rank']) or None,
                                    tagcount = t.findtext('tagcount') and int(t.findtext('tagcount')) or None
                                    ),
                      streamable = (t.findtext('streamable') == '1'),
                      fullTrack = (t.find('streamable').attrib['fulltrack'] == '1'),
                      image = dict([(i.get('size'), i.text) for i in t.findall('image')]),
                      )
                for t in data.findall('track')
                ]

    @LastfmBase.topProperty("topTracks")
    def topTrack(self):
        """top track for the tag"""
        pass
    
    @LastfmBase.cachedProperty
    def playlist(self):
        return Playlist.fetch(self.__api,
                              "lastfm://playlist/tag/%s/freetracks" % self.name)
    
    @staticmethod
    def getTopTags(api):
        params = {'method': 'tag.getTopTags'}
        data = api._fetchData(params).find('toptags')
        return [
                Tag(
                    api,
                    name = t.findtext('name'),
                    url = t.findtext('url'),
                    stats = Stats(
                                  subject = t.findtext('name'),
                                  count = int(t.findtext('count')),
                                  )
                    )
                for t in data.findall('tag')
                ]
    
    @staticmethod
    def search(api,
               tag,
               limit = None):
        params = {'method': 'tag.search', 'tag': tag}
        if limit:
            params.update({'limit': limit})
            
        @lazylist
        def gen(lst):
            data = api._fetchData(params).find('results')
            totalPages = int(data.findtext("{%s}totalResults" % Api.SEARCH_XMLNS))/ \
                            int(data.findtext("{%s}itemsPerPage" % Api.SEARCH_XMLNS)) + 1
            
            @lazylist
            def gen2(lst, data):
                for t in data.findall('tagmatches/tag'):
                    yield Tag(
                              api,
                              name = t.findtext('name'),
                              url = t.findtext('url'),
                              stats = Stats(
                                            subject = t.findtext('name'),
                                            count = int(t.findtext('count')),
                                            )
                              )
                          
            for t in gen2(data):
                yield t
            
            for page in xrange(2, totalPages+1):
                params.update({'page': page})
                data = api._fetchData(params).find('results')
                for t in gen2(data):
                    yield t
        return gen()
    
    @staticmethod
    def hashFunc(*args, **kwds):
        try:
            return hash(kwds['name'])
        except KeyError:
            raise LastfmInvalidParametersError("name has to be provided for hashing")
        
    def __hash__(self):
        return self.__class__.hashFunc(name = self.name)
    
    def __eq__(self, other):
        return self.name == other.name
    
    def __lt__(self, other):
        return self.name < other.name
    
    def __repr__(self):
        return "<lastfm.Tag: %s>" % self.name

from album import Album
from api import Api
from artist import Artist
from error import LastfmInvalidParametersError
from playlist import Playlist
from stats import Stats
from track import Track