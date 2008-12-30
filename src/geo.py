#!/usr/bin/env python

__author__ = "Abhinav Sarkar <abhinav@abhinavsarkar.net>"
__version__ = "0.2"
__license__ = "GNU Lesser General Public License"

from base import LastfmBase
from cacheable import Cacheable
from lazylist import lazylist

class Geo(object):
    """A class representing an geographic location."""
    @staticmethod
    def get_events(api,
                  location,
                  latitude = None,
                  longitude = None,
                  distance = None):
        params = {'method': 'geo.getEvents', 'location': location}
        if distance is not None:
            params.update({'distance': distance})

        if latitude is not None and longitude is not None:
            params.update({'latitude': latitude, 'longitude': longitude})

        @lazylist
        def gen(lst):
            data = api._fetch_data(params).find('events')
            total_pages = int(data.attrib['totalpages'])

            @lazylist
            def gen2(lst, data):
                for e in data.findall('event'):
                    yield Event.create_from_data(api, e)

            for e in gen2(data):
                yield e

            for page in xrange(2, total_pages+1):
                params.update({'page': page})
                data = api._fetch_data(params).find('events')
                for e in gen2(data):
                    yield e
        return gen()

    @staticmethod
    def get_top_artists(api, country):
        params = {'method': 'geo.getTopArtists', 'country': country}
        data = api._fetch_data(params).find('topartists')
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
    def get_top_tracks(api, country, location = None):
        params = {'method': 'geo.getTopTracks', 'country': country}
        if location is not None:
            params.update({'location': location})

        data = api._fetch_data(params).find('toptracks')
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
                       full_track = (t.find('streamable').attrib['fulltrack'] == '1'),
                       url = 'http://' + t.findtext('url'),
                       image = {'large': t.findtext('image')}
                       )
                for t in data.findall('track')
                ]

class Venue(LastfmBase, Cacheable):
    """A class representing a venue of an event"""
    def init(self,
                 name = None,
                 location = None,
                 url = None):
        self._name = name
        self._location = location
        self._url = url

    @property
    def name(self):
        """name of the venue"""
        return self._name

    @property
    def location(self):
        """location of the event"""
        return self._location

    @property
    def url(self):
        """url of the event's page"""
        return self._url

    @staticmethod
    def _hash_func(*args, **kwds):
        try:
            return hash(kwds['url'])
        except KeyError:
            raise InvalidParametersError("url has to be provided for hashing")

    def __hash__(self):
        return self.__class__._hash_func(url = self.url)

    def __eq__(self, other):
        return self.url == other.url

    def __lt__(self, other):
        return self.name < other.name

    def __repr__(self):
        return "<lastfm.geo.Venue: %s, %s>" % (self.name, self.location.city)

class Location(LastfmBase, Cacheable):
    """A class representing a location of an event"""
    XMLNS = "http://www.w3.org/2003/01/geo/wgs84_pos#"

    def init(self,
                 api,
                 city = None,
                 country = None,
                 street = None,
                 postal_code = None,
                 latitude = None,
                 longitude = None,
                 timezone = None):
        if not isinstance(api, Api):
            raise InvalidParametersError("api reference must be supplied as an argument")
        self._api = api
        self._city = city
        self._country = country
        self._street = street
        self._postal_code = postal_code
        self._latitude = latitude
        self._longitude = longitude
        self._timezone = timezone

    @property
    def city(self):
        """city in which the location is situated"""
        return self._city

    @property
    def country(self):
        """country in which the location is situated"""
        return self._country

    @property
    def street(self):
        """street in which the location is situated"""
        return self._street

    @property
    def postal_code(self):
        """postal code of the location"""
        return self._postal_code

    @property
    def latitude(self):
        """latitude of the location"""
        return self._latitude

    @property
    def longitude(self):
        """longitude of the location"""
        return self._longitude

    @property
    def timezone(self):
        """timezone in which the location is situated"""
        return self._timezone

    @LastfmBase.cached_property
    def top_tracks(self):
        """top tracks of the location"""
        if self.country is None or self.city is None:
            raise InvalidParametersError("country and city of this location are required for calling this method")
        return Geo.get_top_tracks(self._api, self.country.name, self.city)

    @LastfmBase.top_property("top_tracks")
    def top_track(self):
        """top track of the location"""
        pass

    def get_events(self,
                  distance = None):
        return Geo.get_events(self._api,
                             self.city,
                             self.latitude,
                             self.longitude,
                             distance)

    @LastfmBase.cached_property
    def events(self):
        """events taking place at/around the location"""
        return self.get_events()

    @staticmethod
    def _hash_func(*args, **kwds):
        try:
            return hash("latlong%s%s" % (kwds['latitude'], kwds['longitude']))
        except KeyError:
            try:
                return hash("name%s" % kwds['city'])
            except KeyError:
                raise InvalidParametersError("either latitude and longitude or city has to be provided for hashing")

    def __hash__(self):
        if not self.city:
            return self.__class__._hash_func(
                                           latitude = self.latitude,
                                           longitude = self.longitude)
        else:
            return self.__class__._hash_func(name = self.city)

    def __eq__(self, other):
        return self.latitude == other.latitude and self.longitude == other.longitude

    def __lt__(self, other):
        if self.country != other.country:
            return self.country < other.country
        else:
            return self.city < other.city

    def __repr__(self):
        if self.city is None:
            return "<lastfm.geo.Location: (%s, %s)>" % (self.latitude, self.longitude)
        else:
            return "<lastfm.geo.Location: %s>" % self.city

class Country(LastfmBase, Cacheable):
    """A class representing a country."""
    def init(self,
                 api,
                 name = None):
        if not isinstance(api, Api):
            raise InvalidParametersError("api reference must be supplied as an argument")
        self._api = api
        self._name = name

    @property
    def name(self):
        """name of the country"""
        return self._name

    @LastfmBase.cached_property
    def top_artists(self):
        """top artists of the country"""
        return Geo.get_top_artists(self._api, self.name)

    @LastfmBase.top_property("top_artists")
    def top_artist(self):
        """top artist of the country"""
        pass

    def get_top_tracks(self, location = None):
        return Geo.get_top_tracks(self._api, self.name, location)

    @LastfmBase.cached_property
    def top_tracks(self):
        """top tracks of the country"""
        return self.get_top_tracks()

    @LastfmBase.top_property("top_tracks")
    def top_track(self):
        """top track of the country"""
        pass

    @LastfmBase.cached_property
    def events(self):
        """events taking place at/around the location"""
        return Geo.get_events(self._api, self.name)

    @staticmethod
    def _hash_func(*args, **kwds):
        try:
            return hash(kwds['name'])
        except KeyError:
            raise InvalidParametersError("name has to be provided for hashing")

    def __hash__(self):
        return self.__class__._hash_func(name = self.name)

    def __eq__(self, other):
        return self.name == other.name

    def __lt__(self, other):
        return self.name < other.name

    def __repr__(self):
        return "<lastfm.geo.Country: %s>" % self.name

from api import Api
from artist import Artist
from error import InvalidParametersError
from event import Event
from stats import Stats
from track import Track
