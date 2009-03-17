#!/usr/bin/env python
"""Module containting the decorators used in the package"""

__author__ = "Abhinav Sarkar <abhinav@abhinavsarkar.net>"
__version__ = "0.2"
__license__ = "GNU Lesser General Public License"
__package__ = "lastfm"

def top_property(list_property_name):
    """
    A decorator to return a property that returns the first value of list 
    attribute corresponding to the provided list property name.
    
    For example, if the list property is top_albums, then the decorator returns
    a property that returns the first (top most) album.
    
    @param list_property_name: the name of the list property. Like 'top_albums'.
    @type list_property_name:  L{str}
    
    @return:                   a property that returns the first value of list attribute 
                               corresponding to the provided list property name
    @rtype:                    L{property}
    """    
    def decorator(func):
        def wrapper(ob):
            top_list = getattr(ob, list_property_name)
            return (len(top_list) and top_list[0] or None)
        return property(fget = wrapper, doc = func.__doc__)
    return decorator

def cached_property(func):
    """
    A decorator to cache the atrribute of the object. When called for the first time,
    the value of the attribute is retrived and saved in an instance variable. Later
    calls return the copy of the cached value, so that the original cached value
    cannot be modified.
    
    @param func:  the getter function of the attribute
    @type func:   C{function}
    
    @return:      a property that wraps the getter function of the attribute
    @rtype:       L{property}
    """
    func_name = func.func_code.co_name
    attribute_name = "_%s" % func_name

    def wrapper(ob):
        cache_attribute = getattr(ob, attribute_name, None)
        if cache_attribute is None:
            cache_attribute = func(ob)
            setattr(ob, attribute_name, cache_attribute)
        try:
            cp = copy.copy(cache_attribute)
            return cp
        except LastfmError:
            return cache_attribute

    return property(fget = wrapper, doc = func.__doc__)

def authenticate(func):
    """
    A decorator to check if the current user is authenticated or not. Used only
    on the functions that need authentication. If not authenticated then an
    exception is raised.
    
    @param func:    a function that needs to be authentication, for being called
    @type func:     C{function}
    
    @return:        a function that wraps the original function
    @rtype:         C{function}
    
    @raise AuthenticationFailedError: If the user is not authenticated, then an
                                      exception is raised.
    """
    def wrapper(self, *args, **kwargs):
        from lastfm.user import User, Api
        username = None
        if isinstance(self, User):
            username = self.name
            if self.authenticated:
               return func(self, *args, **kwargs)
        elif hasattr(self, 'user'):
            username = self.user.name
            if self.user.authenticated:
               return func(self, *args, **kwargs)
        elif hasattr(self, '_subject') and isinstance(self._subject, User):
            username = self._subject.name
            if self._subject.authenticated:
                return func(self, *args, **kwargs)
        elif hasattr(self, '_api') and isinstance(self._api, Api):
            try:
                user = self._api.get_authenticated_user()
                username = user.name
                return func(self, *args, **kwargs)
            except AuthenticationFailedError:
                pass
        raise AuthenticationFailedError(
            "user '%s' does not have permissions to access the service" % username)
    wrapper.__doc__ = func.__doc__
    return wrapper

def depaginate(func):
    from lastfm.lazylist import lazylist
    def wrapper(*args, **kwargs):
        @lazylist
        def generator(lst):
            gen = func(*args, **kwargs)
            total_pages = gen.next()
            for e in gen:
                yield e
            for page in xrange(2, total_pages+1):
                kwargs['page'] = page
                gen = func(*args, **kwargs)
                gen.next()
                for e in gen:
                    yield e
        return generator()
    wrapper.__doc__ = func.__doc__
    return wrapper

import copy
from lastfm.error import LastfmError, AuthenticationFailedError