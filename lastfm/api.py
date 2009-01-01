#!/usr/bin/env python

__author__ = "Abhinav Sarkar <abhinav@abhinavsarkar.net>"
__version__ = "0.2"
__license__ = "GNU Lesser General Public License"

from lastfm.base import LastfmBase

class Api(object):
    """The class representing the last.fm web services API."""

    DEFAULT_CACHE_TIMEOUT = 3600 # cache for 1 hour
    API_ROOT_URL = "http://ws.audioscrobbler.com/2.0/"
    FETCH_INTERVAL = 1
    SEARCH_XMLNS = "http://a9.com/-/spec/opensearch/1.1/"

    def __init__(self,
                 api_key,
                 secret = None,
                 session_key = None,
                 input_encoding=None,
                 request_headers=None,
                 no_cache = False,
                 debug = False):
        self._api_key = api_key
        self._secret = secret
        self._session_key = session_key
        self._cache = FileCache()
        self._urllib = urllib2
        self._cache_timeout = Api.DEFAULT_CACHE_TIMEOUT
        self._initialize_request_headers(request_headers)
        self._initialize_user_agent()
        self._input_encoding = input_encoding
        self._no_cache = no_cache
        self._debug = debug
        self._last_fetch_time = datetime.now()

    @property
    def api_key(self):
        return self._api_key

    @property
    def secret(self):
        return self._secret

    @property
    def session_key(self):
        return self._session_key

    def set_session_key(self):
        params = {'method': 'auth.getSession', 'token': self.auth_token}
        self._session_key = self._fetch_data(params, sign = True).findtext('session/key')
        self._auth_token = None

    @LastfmBase.cached_property
    def auth_token(self):
        params = {'method': 'auth.getToken'}
        return self._fetch_data(params, sign = True).findtext('token')

    @LastfmBase.cached_property
    def auth_url(self):
        return "http://www.last.fm/api/auth/?api_key=%s&token=%s" % (self.api_key, self.auth_token)


    def set_cache(self, cache):
        '''Override the default cache.  Set to None to prevent caching.

        Args:
            cache: an instance that supports the same API as the lastfm.FileCache
        '''
        self._cache = cache

    def set_urllib(self, urllib):
        '''Override the default urllib implementation.

        Args:
            urllib: an instance that supports the same API as the urllib2 module
        '''
        self._urllib = urllib

    def set_cache_timeout(self, cache_timeout):
        '''Override the default cache timeout.

        Args:
            cache_timeout: time, in seconds, that responses should be reused.
        '''
        self._cache_timeout = cache_timeout

    def set_user_agent(self, user_agent):
        '''Override the default user agent

        Args:
        user_agent: a string that should be send to the server as the User-agent
        '''
        self._request_headers['User-Agent'] = user_agent

    def get_album(self,
                 artist = None,
                 album = None,
                 mbid = None):
        if isinstance(artist, Artist):
            artist = artist.name
        return Album.get_info(self, artist, album, mbid)

    def search_album(self,
                     album,
                     limit = None):
        return Album.search(self, search_item = album, limit = limit)

    def get_artist(self,
                  artist = None,
                  mbid = None):
        return Artist.get_info(self, artist, mbid)

    def search_artist(self,
                     artist,
                     limit = None):
        return Artist.search(self, search_item = artist, limit = limit)

    def get_event(self, event):
        return Event.get_info(self, event)

    def get_location(self, name):
        return Location(self, name = name)

    def get_country(self, name):
        return Country(self, name = name)

    def get_group(self, name):
        return Group(self, name = name)

    def get_playlist(self, url):
        return Playlist.fetch(self, url)

    def get_tag(self, name):
        return Tag(self, name = name)

    def get_global_top_tags(self):
        return Tag.get_top_tags(self)

    def search_tag(self,
                  tag,
                  limit = None):
        return Tag.search(self, search_item = tag, limit = limit)

    def compare_taste(self,
                     type1, type2,
                     value1, value2,
                     limit = None):
        return Tasteometer.compare(self, type1, type2, value1, value2, limit)

    def get_track(self, track, artist = None, mbid = None):
        if isinstance(artist, Artist):
            artist = artist.name
        return Track.get_info(self, artist, track, mbid)

    def search_track(self,
                    track,
                    artist = None,
                    limit = None):
        if isinstance(artist, Artist):
            artist = artist.name
        return Track.search(self, search_item = track, limit = limit, artist = artist)

    def get_user(self, name):
        user = None
        try:
            user = User(self, name = name)
            user.friends
        except LastfmError, e:
            raise e
        return user

    def get_authenticated_user(self):
        if self.session_key is not None:
            return User.get_authenticated_user(self)
        return None
    
    def get_venue(self, venue):
        return self.search_venue(venue)[0]
    
    def search_venue(self, venue):
        return Venue.search(self, search_item = venue)

    def _build_url(self, url, path_elements=None, extra_params=None):
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
            extra_query = self._encode_parameters(extra_params)
            # Add it to the existing query
            if query:
                query += '&' + extra_query
            else:
                query = extra_query

        # Return the rebuilt URL
        return urlparse.urlunparse((scheme, netloc, path, params, query, fragment))

    def _initialize_request_headers(self, request_headers):
        if request_headers:
            self._request_headers = request_headers
        else:
            self._request_headers = {}

    def _initialize_user_agent(self):
        user_agent = 'Python-urllib/%s (python-lastfm/%s)' % \
                     (self._urllib.__version__, __version__)
        self.set_user_agent(user_agent)

    def _get_opener(self, url):
        opener = self._urllib.build_opener()
        if self._urllib._opener is not None:
            opener = self._urllib.build_opener(*self._urllib._opener.handlers)
        opener.addheaders = self._request_headers.items()
        return opener

    def _encode(self, s):
        if self._input_encoding:
            return unicode(s, self._input_encoding).encode('utf-8')
        else:
            return unicode(s).encode('utf-8')

    def _encode_parameters(self, parameters):
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
            keys = parameters.keys()
            keys.sort()
            return urllib.urlencode([(k, self._encode(parameters[k])) for k in keys if parameters[k] is not None])

    def _read_url_data(self, opener, url, data = None):
        now = datetime.now()
        delta = now - self._last_fetch_time
        delta = delta.seconds + float(delta.microseconds)/1000000
        if delta < Api.FETCH_INTERVAL:
            time.sleep(Api.FETCH_INTERVAL - delta)
        url_data = opener.open(url, data).read()
        self._last_fetch_time = datetime.now()
        return url_data

    def _fetch_url(self,
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
        url = self._build_url(url, extra_params=parameters)
        if self._debug:
            print url
        # Get a url opener that can handle basic auth
        opener = self._get_opener(url)

        # Open and return the URL immediately if we're not going to cache
        if no_cache or not self._cache or not self._cache_timeout:
            try:
                url_data = self._read_url_data(opener, url)
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
                    url_data = self._read_url_data(opener, url)
                except urllib2.HTTPError, e:
                    url_data = e.read()
                self._cache.Set(key, url_data)
            else:
                url_data = self._cache.Get(key)

        # Always return the latest version
        return url_data

    def _fetch_data(self,
                   params,
                   sign = False,
                   session = False,
                   no_cache = False):
        params = params.copy()
        params['api_key'] = self.api_key

        if session:
            if self.session_key is not None:
                params['sk'] = self.session_key
            else:
                raise AuthenticationFailedError("session key must be present to call this method")

        if sign:
            params['api_sig'] = self._get_api_sig(params)

        xml = self._fetch_url(Api.API_ROOT_URL, params, no_cache = self._no_cache or no_cache)
        return self._check_xml(xml)

    def _post_url(self,
                 url,
                 parameters):
        url = self._build_url(url)
        data = self._encode_parameters(parameters)
        if self._debug:
            print data
        opener = self._get_opener(url)
        url_data = self._read_url_data(opener, url, data)
        return url_data

    def _post_data(self, params):
        params['api_key'] = self.api_key

        if self.session_key is not None:
            params['sk'] = self.session_key
        else:
            raise AuthenticationFailedError("session key must be present to call this method")

        params['api_sig'] = self._get_api_sig(params)
        xml = self._post_url(Api.API_ROOT_URL, params)
        return self._check_xml(xml)

    def _get_api_sig(self, params):
        if self.secret is not None:
                keys = params.keys()[:]
                keys.sort()
                sig = unicode()
                for name in keys:
                    if name == 'api_sig': continue
                    sig += ("%s%s" % (name, params[name]))
                sig += self.secret
                hashed_sig = md5.new(sig).hexdigest()
                return hashed_sig
        else:
            raise AuthenticationFailedError("api secret must be present to call this method")

    def _check_xml(self, xml):
        data = None
        try:
            data = ElementTree.XML(xml)
        except SyntaxError, e:
            raise OperationFailedError("Error in parsing XML: %s" % e)
        if data.get('status') != "ok":
            code = int(data.find("error").get('code'))
            message = data.findtext('error')
            if code in error_map.keys():
                raise error_map[code](message, code)
            else:
                raise LastfmError(message, code)
        return data

    def __repr__(self):
        return "<lastfm.Api: %s>" % self._api_key

from datetime import datetime
import md5
import sys
import time
import urllib
import urllib2
import urlparse

from lastfm.album import Album
from lastfm.artist import Artist
from lastfm.error import error_map, LastfmError, OperationFailedError, AuthenticationFailedError
from lastfm.event import Event
from lastfm.filecache import FileCache
from lastfm.geo import Location, Country
from lastfm.group import Group
from lastfm.playlist import Playlist
from lastfm.tag import Tag
from lastfm.tasteometer import Tasteometer
from lastfm.track import Track
from lastfm.user import User
from lastfm.venue import Venue

if sys.version_info >= (2, 5):
    import xml.etree.cElementTree as ElementTree
else:
    try:
        import cElementTree as ElementTree
    except ImportError:
        try:
            import ElementTree
        except ImportError:
            raise LastfmError("Install ElementTree package for using python-lastfm")
