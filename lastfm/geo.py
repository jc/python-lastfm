#!/usr/bin/env python

__author__ = "Abhinav Sarkar"
__version__ = "0.1"
__license__ = "GNU Lesser General Public License"

class Geo(object):
    """A class representing an geographic location."""
    pass

class Venue(object):
    """A class representing a venue of an event"""
    def __init__(self,
                 event,
                 name = None,
                 location = None,
                 url = None):
        self.__event = event
        self.__name = name
        self.__location = location and Location(
                                                event,
                                                city = location.city,
                                                country = location.country,
                                                street = location.street,
                                                postalCode = location.postalCode,
                                                latitude = location.latitude,
                                                longitude = location.longitude,
                                                timezone = location.timezone
                                                )
        self.__url = url

    def getEvent(self):
        return self.__event

    def getName(self):
        return self.__name

    def getLocation(self):
        return self.__location

    def getUrl(self):
        return self.__url
    
    event = property(getEvent, None, None, "Event's Docstring")

    name = property(getName, None, None, "Name's Docstring")

    location = property(getLocation, None, None, "Location's Docstring")

    url = property(getUrl, None, None, "Url's Docstring")
    
    def __eq__(self, other):
        return sefl.url == other.url
    
class Location(object):
    """A class representing a location of an event"""
    xmlns = "http://www.w3.org/2003/01/geo/wgs84_pos#"
    
    def __init__(self,
                 event,
                 city = None,
                 country = None,
                 street = None,
                 postalCode = None,
                 latitude = None,
                 longitude = None,
                 timezone = None):
        self.__event = event
        self.__city = city
        self.__country = country
        self.__street = street
        self.__postalCode = postalCode
        self.__latitude = latitude
        self.__longitude = longitude
        self.__timezone = timezone

    def getEvent(self):
        return self.__event

    def getCity(self):
        return self.__city

    def getCountry(self):
        return self.__country

    def getStreet(self):
        return self.__street

    def getPostalCode(self):
        return self.__postalCode

    def getLatitude(self):
        return self.__latitude

    def getLongitude(self):
        return self.__longitude

    def getTimezone(self):
        return self.__timezone

    event = property(getEvent, None, None, "Event's Docstring")

    city = property(getCity, None, None, "City's Docstring")

    country = property(getCountry, None, None, "Country's Docstring")

    street = property(getStreet, None, None, "Street's Docstring")

    postalCode = property(getPostalCode, None, None, "PostalCode's Docstring")

    latitude = property(getLatitude, None, None, "Latitude's Docstring")

    longitude = property(getLongitude, None, None, "Longitude's Docstring")

    timezone = property(getTimezone, None, None, "Timezone's Docstring")        
    
    def __eq__(self, other):
        return self.latitude == other.latitude and self.longitude == other.longitude