#!/usr/bin/env python

__author__ = "Abhinav Sarkar"
__version__ = "0.1"
__license__ = "GNU Lesser General Public License"

class Event(object):
    """A class representing an event."""
    def __init__(self,
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
                 attendance = None,
                 reviews = None,
                 tag = None):
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
        self.__attendance = attendance
        self.__reviews = reviews
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

    def getAttendance(self):
        return self.__attendance

    def getReviews(self):
        return self.__reviews

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

    attendance = property(getAttendance, None, None, "Attendance's Docstring")

    reviews = property(getReviews, None, None, "Reviews's Docstring")

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
                     headliner = data.findtext('artists/headliner'),
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
                     startDate = datetime(*(time.strptime(data.findtext('startDate').strip(), '%a, %d %b %Y')[0:6])),
                     startTime = datetime(*(time.strptime(data.findtext('startTime').strip(), '%H:%M')[0:6])),
                     description = data.findtext('description'),
                     image = dict([(i.get('size'), i.text) for i in data.findall('image')]),
                     url = data.findtext('url'),
                     attendance = int(data.findtext('attendance')),
                     reviews = int(data.findtext('reviews')),
                     tag = data.findtext('tag')
                    )
    def __eq__(self, other):
        return self.id == other.id
        
from datetime import datetime
import time

from artist import Artist
from geo import Venue, Location, Country