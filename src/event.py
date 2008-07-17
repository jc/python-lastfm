#!/usr/bin/env python

__author__ = "Abhinav Sarkar"
__version__ = "0.1"
__license__ = "GNU Lesser General Public License"

from base import LastfmBase

class Event(LastfmBase):
    """A class representing an event."""
    def init(self,
                 api,
                 id = None,
                 title = None,
                 artists = None,
                 headliner = None,
                 venue = None,
                 startDate = None,
                 startTime = None,
                 description = None,
                 image = None,
                 url = None,
                 stats = None,
                 tag = None):
        if not isinstance(api, Api):
            raise LastfmError("api reference must be supplied as an argument")
        self.__api = api
        self.__id = id
        self.__title = title
        self.__artists = artists
        self.__headliner = headliner
        self.__venue = venue
        self.__startDate = startDate
        self.__startTime = startTime
        self.__description = description
        self.__image = image
        self.__url = url
        self.__stats = stats and Stats(
                             subject = self,
                             attendance = self.attendance,
                             reviews = self.reviews
                            )
        self.__tag = tag

    def getId(self):
        return self.__id

    def getTitle(self):
        return self.__title

    def getArtists(self):
        return self.__artists
    
    def getHeadliner(self):
        return self.__headliner

    def getVenue(self):
        return self.__venue

    def getStartDate(self):
        return self.__startDate

    def getStartTime(self):
        return self.__startTime

    def getDescription(self):
        return self.__description

    def getImage(self):
        return self.__image

    def getUrl(self):
        return self.__url

    def getStats(self):
        return self.__stats

    def getTag(self):
        return self.__tag
        
    id = property(getId, None, None, "Id's Docstring")

    title = property(getTitle, None, None, "Title's Docstring")

    artists = property(getArtists, None, None, "Artists's Docstring")
    
    headliner = property(getHeadliner, None, None, "headliner's Docstring")

    venue = property(getVenue, None, None, "Venue's Docstring")

    startDate = property(getStartDate, None, None, "StartDate's Docstring")

    startTime = property(getStartTime, None, None, "StartTime's Docstring")

    description = property(getDescription, None, None, "Description's Docstring")

    image = property(getImage, None, None, "Image's Docstring")

    url = property(getUrl, None, None, "Url's Docstring")

    stats = property(getStats, None, None, "Match's Docstring")
    
    tag = property(getTag, None, None, "Tag's Docstring")        
    
    @staticmethod
    def getInfo(api, event):
        params = {'method': 'event.getinfo', 'event': event}
        data = api.fetchData(params).find('event')
    
        return Event(
                     api,
                     id = int(data.findtext('id')),
                     title = data.findtext('title'),
                     artists = [Artist(api, name = a.text) for a in data.findall('artists/artist')],
                     headliner = Artist(api, name = data.findtext('artists/headliner')),
                     venue = Venue(
                                   name = data.findtext('venue/name'),
                                   location = Location(
                                                       api,
                                                       city = data.findtext('venue/location/city'),
                                                       country = Country(
                                                            api,
                                                            name = data.findtext('venue/location/country')
                                                            ),
                                                       street = data.findtext('venue/location/street'),
                                                       postalCode = data.findtext('venue/location/postalcode'),
                                                       latitude = float(data.findtext(
                                                           'venue/location/{%s}point/{%s}lat' % ((Location.xmlns,)*2)
                                                           )),
                                                       longitude = float(data.findtext(
                                                           'venue/location/{%s}point/{%s}long' % ((Location.xmlns,)*2)
                                                           )),
                                                       timezone = data.findtext('venue/location/timezone')
                                                       ),
                                   url = data.findtext('venue/url')
                                   ),
                     startDate = data.findtext('startDate') and 
                                    datetime(*(time.strptime(data.findtext('startDate').strip(), '%a, %d %b %Y')[0:6])) or
                                    None,
                     startTime = data.findtext('startTime') and 
                                    datetime(*(time.strptime(data.findtext('startTime').strip(), '%H:%M')[0:6])) or
                                    None,
                     description = data.findtext('description'),
                     image = dict([(i.get('size'), i.text) for i in data.findall('image')]),
                     url = data.findtext('url'),
                     stats = Stats(
                                   subject = int(data.findtext('id')),
                                   attendance = int(data.findtext('attendance')),
                                   reviews = int(data.findtext('reviews')),
                                   ),
                     tag = data.findtext('tag')
                    )
        
    @staticmethod
    def hashFunc(*args, **kwds):
        try:
            return hash(kwds['id'])
        except KeyError:
            raise LastfmError("id has to be provided for hashing")
        
    def __hash__(self):
        return Event.hashFunc(id = self.id)
    
    def __eq__(self, other):
        return self.id == other.id
    
    def __lt__(self, other):
        return self.startDate < other.startDate
    
    def __repr__(self):
        return "<lastfm.Event: %s at %s on %s>" % (self.title, self.venue.name, self.startDate.strftime("%x"))
        
from datetime import datetime
import time

from api import Api
from error import LastfmError
from artist import Artist
from geo import Venue, Location, Country
from stats import Stats