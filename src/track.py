#!/usr/bin/env python

__author__ = "Abhinav Sarkar <abhinav@abhinavsarkar.net>"
__version__ = "0.2"
__license__ = "GNU Lesser General Public License"

from base import LastfmBase
from lazylist import lazylist

class Track(LastfmBase):
    """A class representing a track."""
    def init(self,
                 api,
                 name = None,
                 mbid = None,
                 url = None,
                 streamable = None,
                 artist = None,
                 album = None,
                 image = None,
                 stats = None,
                 fullTrack = None,
                 playedOn = None,
                 lovedOn = None):
        if not isinstance(api, Api):
            raise LastfmInvalidParametersError("api reference must be supplied as an argument")
        self.__api = api
        self.__name = name
        self.__mbid = mbid
        self.__url = url
        self.__streamable = streamable
        self.__artist = artist
        self.__album = album
        self.__image = image
        self.__stats = stats and Stats(
                             subject = self,
                             match = stats.match,
                             playcount = stats.playcount,
                             rank = stats.rank,
                             listeners = stats.listeners,
                            )
        self.__fullTrack = fullTrack
        self.__playedOn = playedOn
        self.__lovedOn = lovedOn
        self.__tags = None
        
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
    def album(self):
        """artist of the track"""
        return self.__album

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

    @property
    def playedOn(self):
        """datetime the track was last played"""
        return self.__playedOn

    @property
    def lovedOn(self):
        """datetime the track was marked 'loved'"""
        return self.__lovedOn

    def __checkParams(self,
                      params,
                      artist = None,
                      track = None,
                      mbid = None):
        if not ((artist and track) or mbid):
            raise LastfmInvalidParametersError("either (artist and track) or mbid has to be given as argument.")

        if artist and track:
            params.update({'artist': artist, 'track': track})
        elif mbid:
            params.update({'mbid': mbid})
        return params

    @LastfmBase.cachedProperty
    def similar(self):
        """tracks similar to this track"""
        params = self.__checkParams(
                                    {'method': 'track.getSimilar'},
                                    self.artist.name,
                                    self.name,
                                    self.mbid
                                    )
        data = self.__api._fetchData(params).find('similartracks')
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

    @LastfmBase.topProperty("similar")
    def mostSimilar(self):
        """track most similar to this track"""
        pass

    @LastfmBase.cachedProperty
    def topFans(self):
        """top fans of the track"""
        params = self.__checkParams(
                                    {'method': 'track.getTopFans'},
                                    self.artist.name,
                                    self.name,
                                    self.mbid
                                    )
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
        """topmost fan of the track"""
        pass

    @LastfmBase.cachedProperty
    def topTags(self):
        """top tags for the track"""
        params = self.__checkParams(
                                    {'method': 'track.getTopTags'},
                                    self.artist.name,
                                    self.name,
                                    self.mbid
                                    )
        data = self.__api._fetchData(params).find('toptags')
        return [
                Tag(
                    self.__api,
                    subject = self,
                    name = t.findtext('name'),
                    url = t.findtext('url'),
                    stats = Stats(
                                  subject = t.findtext('name'),
                                  count = int(t.findtext('count')),
                                  )
                    )
                for t in data.findall('tag')
                ]

    @LastfmBase.topProperty("topTags")
    def topTag(self):
        """topmost tag for the track"""
        pass
    
    @LastfmBase.cachedProperty
    def tags(self):
        if self.__tags is None:
            if not (self.artist and self.name):
                raise LastfmInvalidParametersError("artist and track name have to be provided.")
            params = {'method': 'track.getTags', 'artist': self.artist.name, 'track': self.name}
            data = self.__api._fetchData(params, sign = True, session = True, no_cache = True).find('tags')
            self.__tags = SafeList([
                           Tag(
                               self.__api,
                               name = t.findtext('name'),
                               url = t.findtext('url')
                               )
                           for t in data.findall('tag')
                           ],
                           self.addTags, self.removeTag)
        return self.__tags
    
    def addTags(self, tags):
        while(len(tags) > 10):
                        section = tags[0:9]
                        tags = tags[9:]
                        self.addTags(section)
        
        if len(tags) == 0: return

        tagnames = []
        for tag in tags:
            if isinstance(tag, Tag):
                tagnames.append(tag.name)
            elif isinstance(tag, str):
                tagnames.append(tag)
                
        params = {
                  'method': 'track.addTags',
                  'artist': self.artist.name,
                  'track': self.name,
                  'tags': ",".join(tagnames)
                  }
        
        self.__api._postData(params)
        self.__tags = None
        
    def removeTag(self, tag):
        if isinstance(tag, Tag):
            tag = tag.name
        params = {
                  'method': 'track.removeTag',
                  'artist': self.artist.name,
                  'track': self.name,
                  'tag': tag
                  }
        self.__api._postData(params)
        self.__tags = None
    
    def love(self):
        params = {'method': 'track.love', 'artist': self.artist.name, 'track': self.name}
        self.__api._postData(params)
        
    def ban(self):
        params = {'method': 'track.ban', 'artist': self.artist.name, 'track': self.name}
        self.__api._postData(params)
        
    def share(self, recipient, message = None):
        params = {
                  'method': 'track.share',
                  'artist': self.artist.name,
                  'track': self.name
                  }
        if message is not None:
            params['message'] = message
        
        for i in xrange(len(recipient)):
            if isinstance(recipient[i], User):
                recipient[i] = recipient[i].name
        params['recipient'] = ",".join(recipient)
        self.__api._postData(params)

    @staticmethod
    def search(api,
               track,
               artist = None,
               limit = None):
        params = {'method': 'track.search', 'track': track}
        if artist is not None:
            params.update({'artist': artist})
        if limit is not None:
            params.update({'limit': limit})
            
        @lazylist
        def gen(lst):
            data = api._fetchData(params).find('results')
            totalPages = int(data.findtext("{%s}totalResults" % Api.SEARCH_XMLNS))/ \
                            int(data.findtext("{%s}itemsPerPage" % Api.SEARCH_XMLNS)) + 1
            
            @lazylist
            def gen2(lst, data):
                for t in data.findall('trackmatches/track'):
                    yield Track(
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
            return hash("%s%s" % (kwds['name'], hash(kwds['artist'])))
        except KeyError:
            raise LastfmInvalidParametersError("name and artist have to be provided for hashing")

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
from error import LastfmInvalidParametersError
from safelist import SafeList
from stats import Stats
from tag import Tag
from user import User