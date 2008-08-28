#!/usr/bin/env python

__author__ = "Abhinav Sarkar <abhinav@abhinavsarkar.net>"
__version__ = "0.1"
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
            
        if 'bypassRegistry' in kwds:
                del kwds['bypassRegistry']
                inst = object.__new__(cls)
                inst.init(*args, **kwds)
                return inst

        key = cls.hashFunc(*args, **kwds)
        if subject is not None:
            key = (hash(subject), key)
            
        LastfmBase._lock.acquire()
        try:
            inst, alreadyRegistered = LastfmBase.register(object.__new__(cls), key)
            if not alreadyRegistered:
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
    def topProperty(listPropertyName):
        def decorator(func):
            def wrapper(ob):
                topList = getattr(ob, listPropertyName)
                return (len(topList) and topList[0] or None)
            return property(fget = wrapper, doc = func.__doc__)
        return decorator
    
    @staticmethod
    def cachedProperty(func):
        frame = sys._getframe(1)
        classname = frame.f_code.co_name
        funcName = func.func_code.co_name
        attributeName = "_%s__%s" % (classname, funcName)
        
        def wrapper(ob):
            cacheAttribute = getattr(ob, attributeName, None)
            if cacheAttribute is None:
                cacheAttribute = func(ob)
                setattr(ob, attributeName, cacheAttribute)
            return cacheAttribute
        
        return property(fget = wrapper, doc = func.__doc__)

    def __gt__(self, other):
        return not (self.__lt__(other) or self.__eq(other))

    def __ne__(self, other):
        return not self.__eq__(other)

    def __ge__(self, other):
        return not self.__lt__(other)

    def __le__(self, other):
        return not self.__gt__(other)

import sys