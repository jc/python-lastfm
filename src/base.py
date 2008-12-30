#!/usr/bin/env python

__author__ = "Abhinav Sarkar <abhinav@abhinavsarkar.net>"
__version__ = "0.2"
__license__ = "GNU Lesser General Public License"

try:
    from threading import Lock
except ImportError:
    from dummy_threading import Lock

class LastfmBase(object):
    """Base class for all the classes in this package"""

    registry = {}
    _lock = Lock()

    def __new__(cls, *args, **kwds):
        subject = None
        if 'subject' in kwds and not cls.__name__.startswith('Weekly'):
            subject = kwds['subject']
            del kwds['subject']

        if 'bypass_registry' in kwds:
                del kwds['bypass_registry']
                inst = object.__new__(cls)
                inst.init(*args, **kwds)
                return inst

        key = cls._hash_func(*args, **kwds)
        if subject is not None:
            key = (hash(subject), key)

        LastfmBase._lock.acquire()
        try:
            inst, already_registered = LastfmBase.register(object.__new__(cls), key)
            if not already_registered:
                inst.init(*args, **kwds)
        finally:
            LastfmBase._lock.release()
        return inst

    @staticmethod
    def register(ob, key):
        if not ob.__class__ in LastfmBase.registry:
            LastfmBase.registry[ob.__class__] = {}
        if key in LastfmBase.registry[ob.__class__]:
            ob = LastfmBase.registry[ob.__class__][key]
            #print "already registered: %s" % repr(ob)
            return (ob, True)
        else:
            #print "not already registered: %s" % ob.__class__
            LastfmBase.registry[ob.__class__][key] = ob
            return (ob, False)

    @staticmethod
    def top_property(list_property_name):
        def decorator(func):
            def wrapper(ob):
                top_list = getattr(ob, list_property_name)
                return (len(top_list) and top_list[0] or None)
            return property(fget = wrapper, doc = func.__doc__)
        return decorator

    @staticmethod
    def cached_property(func):
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
            except Error:
                return cache_attribute

        return property(fget = wrapper, doc = func.__doc__)

    def __gt__(self, other):
        return not (self.__lt__(other) or self.__eq(other))

    def __ne__(self, other):
        return not self.__eq__(other)

    def __ge__(self, other):
        return not self.__lt__(other)

    def __le__(self, other):
        return not self.__gt__(other)

import copy
from error import Error
