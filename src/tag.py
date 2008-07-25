#!/usr/bin/env python

__author__ = "Abhinav Sarkar"
__version__ = "0.1"
__license__ = "GNU Lesser General Public License"

from base import LastfmBase

class Tag(LastfmBase):
    """"A class representing a tag."""
    def init(self,
                 api,
                 name = None,
                 url = None,
                 streamable = None):
        if not isinstance(api, Api):
            raise LastfmError("api reference must be supplied as an argument")
        self.__api = api
        self.__name = name
        self.__url = url
        self.__streamable = streamable
        self.__similar = None
        self.__topAlbums = None
        self.__topArtists = None
        self.__topTracks = None
    
    def getName(self):
        return self.__name

    def getUrl(self):
        return self.__url
    
    def isStreamable(self):
        return self.__streamable
    
    name = property(getName, None, None, "Name's Docstring")

    url = property(getUrl, None, None, "Url's Docstring")
    
    streamable = property(isStreamable, None, None, "Docstring")
    
    def getSimilar(self):
        if self.__similar is None:
            params = {'method': 'tag.getsimilar', 'tag': self.name}
            data = self.__api._fetchData(params).find('similartags')
            self.__similar = [
                              Tag(
                                  self.__api,
                                  name = t.findtext('name'),
                                  url = t.findtext('url'),
                                  streamable = (t.findtext('streamable') == "1"),
                                  )
                              for t in data.findall('tag')
                              ]
        return self.__similar
    
    similar = property(getSimilar, None, None, "Docstring")
    
    def getTopAlbums(self):
        if self.__topAlbums is None:
            params = {'method': 'tag.gettopalbums', 'tag': self.name}
            data = self.__api._fetchData(params).find('topalbums')
            self.__topAlbums = [
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
                                                    tagcount = a.findtext('tagcount') and int(a.findtext('tagcount')) or None,
                                                    rank = a.attrib['rank'].strip() and int(a.attrib['rank']) or None
                                                    )
                                      )
                                for a in data.findall('album')
                                ]
        return self.__topAlbums
    
    topAlbums = property(getTopAlbums, None, None, "Docstring")
    topAlbum = property(
                         lambda self: len(self.topAlbums) and self.topAlbums[0] or None,
                         None, None, "Docstring"                         
                         )
    
    def getTopArtists(self):
        if self.__topArtists is None:
            params = {'method': 'tag.gettopartists', 'tag': self.name}
            data = self.__api._fetchData(params).find('topartists')
            self.__topArtists = [
                                 Artist(
                                        self.__api,
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
        return self.__topArtists
            
    topArtists = property(getTopArtists, None, None, "Docstring")
    topArtist = property(
                         lambda self: len(self.topArtists) and self.topArtists[0] or None,
                         None, None, "Docstring"                         
                         )
    
    def getTopTracks(self):
        if self.__topTracks is None:
            params = {'method': 'tag.gettoptracks', 'tag': self.name}
            data = self.__api._fetchData(params).find('toptracks')
            self.__topTracks = [
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
                                                    tagcount = t.findtext('tagcount') and int(t.findtext('tagcount')) or None
                                                    ),
                                      streamable = (t.findtext('streamable') == '1'),
                                      fullTrack = (t.find('streamable').attrib['fulltrack'] == '1'),
                                      image = dict([(i.get('size'), i.text) for i in t.findall('image')]),
                                      )
                                for t in data.findall('track')
                                ]
        return self.__topTracks
    
    topTracks = property(getTopTracks, None, None, "Docstring")
    topTrack = property(lambda self: len(self.topTracks) and self.topTracks[0],
                   None, None, "docstring")
    
    @staticmethod
    def getTopTags(api):
        pass
    
    @staticmethod
    def search(api,
               tag,
               limit = None,
               page = None):
        pass
    
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
        return "<lastfm.Tag: %s>" % self.name

from api import Api
from error import LastfmError
from album import Album
from artist import Artist
from track import Track
from stats import Stats