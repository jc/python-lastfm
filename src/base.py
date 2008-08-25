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
        if 'bypassRegistry' in kwds:
                del kwds['bypassRegistry']
                inst = object.__new__(cls)
                inst.init(*args, **kwds)
                return inst

        key = cls.hashFunc(*args, **kwds)
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
    

    def __gt__(self, other):
        return not (self.__lt__(other) or self.__eq(other))

    def __ne__(self, other):
        return not self.__eq__(other)

    def __ge__(self, other):
        return not self.__lt__(other)

    def __le__(self, other):
        return not self.__gt__(other)
