#!/usr/bin/env python

__author__ = "Abhinav Sarkar"
__version__ = "0.1"
__license__ = "GNU Lesser General Public License"

class Api(object):
    """The class representing the last.fm web services API."""
    
    DEFAULT_CACHE_TIMEOUT = 3600 # cache for 1 hour
    API_ROOT_URL = "http://ws.audioscrobbler.com/2.0/"

    def __init__(self,
                 apiKey = '23caa86333d2cb2055fa82129802780a',
                 input_encoding=None,
                 request_headers=None,
                 no_cache = False,
                 debug = False):
        self.__apiKey = apiKey
        self._cache = FileCache()
        self._urllib = urllib2
        self._cache_timeout = Api.DEFAULT_CACHE_TIMEOUT
        self._InitializeRequestHeaders(request_headers)
        self._InitializeUserAgent()
        self._input_encoding = input_encoding
        self._no_cache = no_cache
        self._debug = debug

    def getApiKey(self):
        return self.__apiKey
    
    def setCache(self, cache):
        '''Override the default cache.  Set to None to prevent caching.

        Args:
            cache: an instance that supports the same API as the audioscrobblerws.FileCache
        '''
        self._cache = cache

    def setUrllib(self, urllib):
        '''Override the default urllib implementation.

        Args:
            urllib: an instance that supports the same API as the urllib2 module
        '''
        self._urllib = urllib

    def setCacheTimeout(self, cache_timeout):
        '''Override the default cache timeout.

        Args:
            cache_timeout: time, in seconds, that responses should be reused.
        '''
        self._cache_timeout = cache_timeout

    def setUserAgent(self, user_agent):
        '''Override the default user agent

        Args:
        user_agent: a string that should be send to the server as the User-agent
        '''
        self._request_headers['User-Agent'] = user_agent

    def _BuildUrl(self, url, path_elements=None, extra_params=None):
        # Break url into consituent parts
        (scheme, netloc, path, params, query, fragment) = urlparse.urlparse(url)
        path = path.replace(' ', '+')

        # Add any additional path elements to the path
        if path_elements:
            # Filter out the path elements that have a value of None
            p = [i for i in path_elements if i]
            if not path.endswith('/'):
                path += '/'
                path += '/'.join(p)

        # Add any additional query parameters to the query string
        if extra_params and len(extra_params) > 0:
            extra_query = self._EncodeParameters(extra_params)
            # Add it to the existing query
            if query:
                query += '&' + extra_query
            else:
                query = extra_query

        # Return the rebuilt URL
        return urlparse.urlunparse((scheme, netloc, path, params, query, fragment))

    def _InitializeRequestHeaders(self, request_headers):
        if request_headers:
            self._request_headers = request_headers
        else:
            self._request_headers = {}

    def _InitializeUserAgent(self):
        user_agent = 'Python-urllib/%s (python-lastfm/%s)' % \
                     (self._urllib.__version__, __version__)
        self.setUserAgent(user_agent)

    def _GetOpener(self, url):
        opener = self._urllib.build_opener()
        opener.addheaders = self._request_headers.items()
        return opener

    def _Encode(self, s):
        if self._input_encoding:
            return unicode(s, self._input_encoding).encode('utf-8')
        else:
            return unicode(s).encode('utf-8')

    def _EncodeParameters(self, parameters):
        '''Return a string in key=value&key=value form

            Values of None are not included in the output string.

            Args:
                parameters:
                    A dict of (key, value) tuples, where value is encoded as
                    specified by self._encoding
            Returns:
                A URL-encoded string in "key=value&key=value" form
        '''
        if parameters is None:
            return None
        else:
            return urllib.urlencode(dict([(k, self._Encode(v)) for k, v in parameters.items() if v is not None]))
        
    def getAlbum(self,
                 artist = None,
                 album = None,
                 mbid = None):
        if isinstance(artist, Artist):
            artist = artist.name
        return Album.getInfo(self, artist, album, mbid)
    
    def getArtist(self,
                  artist = None,
                  mbid = None):
        return Artist.getInfo(self, artist, mbid)
    
    def searchArtist(self,
                     artist,
                     limit = None,
                     page = None):
        return Artist.search(self, artist, limit, page)
    
    def getEvent(self, event):
        return Event.getInfo(self, event)
    
    def getLocation(self, name):
        return Location(self, name = name)
    
    def getCountry(self, name):
        return Country(self, name = name)
    
    def getGroup(self, name):
        return Group(self, name = name)
    
    def fetchPlaylist(self, url):
        return Playlist.fetch(self, url)
    
    def getTag(self, name):
        return Tag(self, name = name)
    
    def getGlobalTopTags(self):
        return Tag.getTopTags(self)
    
    def searchTag(self,
                  tag,
                  limit = None,
                  page = None):
        return Tag.search(self, tag, limit, page)
    
    def compareTaste(self,
                     type1, type2,
                     value1, value2,
                     limit = None):
        return Tasteometer.compare(self, type1, type2, value1, value2, limit)
    
    def getTrack(self, track, artist):
        if isinstance(artist, Artist):
            artist = artist.name
        result = Track.search(self, track, artist)
        if len(result.matches) == 0:
            raise LastfmError("'%s' by %s: no such track found" % (track, artist))
        return result.matches[0]
    
    def searchTrack(self,
                    track,
                    artist = None,
                    limit = None,
                    page = None):
        if isinstance(artist, Artist):
            artist = artist.name
        return Track.search(self, track, artist, limit, page)
    
    def getUser(self, name):
        return User(self, name = name)

    def _fetchUrl(self,
                  url,
                  parameters = None,
                  no_cache = False):
        '''Fetch a URL, optionally caching for a specified time.

        Args:
            url: The URL to retrieve
            parameters: A dict of key/value pairs that should added to
                        the query string. [OPTIONAL]
            no_cache: If true, overrides the cache on the current request

        Returns:
            A string containing the body of the response.
        '''
        # Add key/value parameters to the query string of the url
        url = self._BuildUrl(url, extra_params=parameters)
        if self._debug:
            print url
        # Get a url opener that can handle basic auth
        opener = self._GetOpener(url)

        # Open and return the URL immediately if we're not going to cache
        if no_cache or not self._cache or not self._cache_timeout:
            try:
                url_data = opener.open(url).read()
            except urllib2.HTTPError, e:
                url_data = e.read()
        else:
            # Unique keys are a combination of the url and the username
            key = url.encode('utf-8')

            # See if it has been cached before
            last_cached = self._cache.GetCachedTime(key)

            # If the cached version is outdated then fetch another and store it
            if not last_cached or time.time() >= last_cached + self._cache_timeout:
                try:
                    url_data = opener.open(url).read()
                except urllib2.HTTPError, e:
                    url_data = e.read()
                self._cache.Set(key, url_data)
            else:
                url_data = self._cache.Get(key)

        # Always return the latest version
        return url_data
    
    def _fetchData(self, params, parse = True):
        params.update({'api_key': self.__apiKey})
        xml = self._fetchUrl(Api.API_ROOT_URL, params, no_cache = self._no_cache)
        #print xml
        try:
            data = ElementTree.XML(xml)
        except SyntaxError, e:
            raise LastfmError("Error in parsing XML: %s" % e)
        if data.get('status') != "ok":
            raise LastfmError("Error code: %s (%s)" % (data.find("error").get('code'), data.findtext('error')))
        if parse:
            return data
        else:
            return xml
        
    def __repr__(self):
        return "<lastfm.Api: %s>" % self.__apiKey
    
import sys
import time
import urllib
import urllib2
import urlparse

from album import Album
from artist import Artist
from error import LastfmError
from event import Event
from filecache import FileCache
from geo import Location, Country
from group import Group
from playlist import Playlist
from tag import Tag
from tasteometer import Tasteometer
from track import Track
from user import User

if sys.version.startswith('2.5'):
    import xml.etree.cElementTree as ElementTree
else:
    try:
        import cElementTree as ElementTree
    except ImportError:
        try:
            import ElementTree
        except ImportError:
            raise LastfmError("Install ElementTree package for using python-lastfm")