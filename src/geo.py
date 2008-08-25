#!/usr/bin/env python

__author__ = "Abhinav Sarkar <abhinav@abhinavsarkar.net>"
__version__ = "0.1"
__license__ = "GNU Lesser General Public License"

from base import LastfmBase

class Geo(object):
    """A class representing an geographic location."""
    @staticmethod
    def getEvents(api,
                  location,
                  distance = None,
                  page = None):
        params = {'method': 'geo.getevents', 'location': location}
        if distance is not None:
            params.update({'distance': distance})
            
        if page is not None:
            params.update({'page': page})

        data = api._fetchData(params).find('events')

        return SearchResult(
                            type = 'event',
                            searchTerms = data.attrib['location'],
                            startPage = int(data.attrib['page']),
                            totalResults = int(data.attrib['total']),
                            itemsPerPage = int(math.ceil(float(data.attrib['total']))/float(data.attrib['totalpages'])),
                            matches = [
                                Event.createFromData(api, e)
                                for e in data.findall('event')
                                ]
                        )

    @staticmethod
    def getTopArtists(api, country):
        params = {'method': 'geo.gettopartists', 'country': country}
        data = api._fetchData(params).find('topartists')
        return [
                Artist(
                       api,
                       name = a.findtext('name'),
                       mbid = a.findtext('mbid'),
                       stats = Stats(
                                     subject = a.findtext('name'),
                                     rank = int(a.attrib['rank']),
                                     playcount = int(a.findtext('playcount'))
                                     ),
                       url = 'http://' + a.findtext('url'),
                       image = {'large': a.findtext('image')}
                       )
                for a in data.findall('artist')
                ]

    @staticmethod
    def getTopTracks(api, country):
        params = {'method': 'geo.gettoptracks', 'country': country}
        data = api._fetchData(params).find('toptracks')
        return [
                Track(
                       api,
                       name = t.findtext('name'),
                       mbid = t.findtext('mbid'),
                       artist = Artist(
                                       api,
                                       name = t.findtext('artist/name'),
                                       mbid = t.findtext('artist/mbid'),
                                       url = t.findtext('artist/url')
                                       ),
                       stats = Stats(
                                     subject = t.findtext('name'),
                                     rank = int(t.attrib['rank']),
                                     playcount = int(t.findtext('playcount'))
                                     ),
                       streamable = (t.findtext('streamable') == '1'),
                       fullTrack = (t.find('streamable').attrib['fulltrack'] == '1'),
                       url = 'http://' + t.findtext('url'),
                       image = {'large': t.findtext('image')}
                       )
                for t in data.findall('track')
                ]

class Venue(LastfmBase):
    """A class representing a venue of an event"""
    def init(self,
                 name = None,
                 location = None,
                 url = None):
        self.__name = name
        self.__location = location
        self.__url = url

    @property
    def name(self):
        """name of the venue"""
        return self.__name

    @property
    def location(self):
        """location of the event"""
        return self.__location

    @property
    def url(self):
        """url of the event's page"""
        return self.__url

    @staticmethod
    def hashFunc(*args, **kwds):
        try:
            return hash(kwds['url'])
        except KeyError:
            raise LastfmError("url has to be provided for hashing")

    def __hash__(self):
        return self.__class__.hashFunc(url = self.url)

    def __eq__(self, other):
        return self.url == other.url

    def __lt__(self, other):
        return self.name < other.name

    def __repr__(self):
        return "<lastfm.geo.Venue: %s, %s>" % (self.name, self.location.city)

class Location(LastfmBase):
    """A class representing a location of an event"""
    xmlns = "http://www.w3.org/2003/01/geo/wgs84_pos#"

    def init(self,
                 api,
                 name = None,
                 city = None,
                 country = None,
                 street = None,
                 postalCode = None,
                 latitude = None,
                 longitude = None,
                 timezone = None):
        if not isinstance(api, Api):
            raise LastfmError("api reference must be supplied as an argument")
        self.__api = api
        self.__name = name
        self.__city = city
        self.__country = country
        self.__street = street
        self.__postalCode = postalCode
        self.__latitude = latitude
        self.__longitude = longitude
        self.__timezone = timezone

    @property
    def name(self):
        """name of the location"""
        return self.__name

    @property
    def city(self):
        """city in which the location is situated"""
        return self.__city

    @property
    def country(self):
        """country in which the location is situated"""
        return self.__country

    @property
    def street(self):
        """street in which the location is situated"""
        return self.__street

    @property
    def postalCode(self):
        """postal code of the location"""
        return self.__postalCode

    @property
    def latitude(self):
        """latitude of the location"""
        return self.__latitude

    @property
    def longitude(self):
        """longitude of the location"""
        return self.__longitude

    @property
    def timezone(self):
        """timezone in which the location is situated"""
        return self.__timezone

    def getEvents(self,
                  distance = None,
                  page = None):
        return Geo.getEvents(self.__api, self.name, distance, page).matches

    @LastfmBase.cachedProperty
    def events(self):
        """events taking place at/around the location"""
        return self.getEvents()
        
    @staticmethod
    def hashFunc(*args, **kwds):
        try:
            return hash("latlong%s%s" % (kwds['latitude'], kwds['longitude']))
        except KeyError:
            try:
                return hash("name%s" % kwds['name'])
            except KeyError:
                raise LastfmError("either latitude and longitude or name has to be provided for hashing")

    def __hash__(self):
        if not self.name:
            return self.__class__.hashFunc(
                                           latitude = self.latitude,
                                           longitude = self.longitude)
        else:
            return self.__class__.hashFunc(name = self.name)

    def __eq__(self, other):
        return self.latitude == other.latitude and self.longitude == other.longitude

    def __lt__(self, other):
        if self.country != other.country:
            return self.country < other.country
        else:
            return self.city < other.city

    def __repr__(self):
        if self.name is None:
            return "<lastfm.geo.Location: (%s, %s)>" % (self.latitude, self.longitude)
        else:
            return "<lastfm.geo.Location: %s>" % self.name

class Country(LastfmBase):
    """A class representing a country."""
    def init(self,
                 api,
                 name = None):
        if not isinstance(api, Api):
            raise LastfmError("api reference must be supplied as an argument")
        self.__api = api
        self.__name = name

    @property
    def name(self):
        """name of the country"""
        return self.__name

    @LastfmBase.cachedProperty
    def topArtists(self):
        """top artists of the country"""
        return Geo.getTopArtists(self.__api, self.name)
        
    @LastfmBase.topProperty("topArtists")
    def topArtist(self):
        """top artist of the country"""
        pass

    @LastfmBase.cachedProperty
    def topTracks(self):
        """top tracks of the country"""
        return Geo.getTopTracks(self.__api, self.name)
        
    @LastfmBase.topProperty("topTracks")
    def topTrack(self):
        """top track of the country"""
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
        return "<lastfm.geo.Country: %s>" % self.name

import math

from api import Api
from artist import Artist
from error import LastfmError
from event import Event
from search import SearchResult
from stats import Stats
from track import Track
