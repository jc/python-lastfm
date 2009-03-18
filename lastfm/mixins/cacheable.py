#!/usr/bin/env python

__author__ = "Abhinav Sarkar <abhinav@abhinavsarkar.net>"
__version__ = "0.2"
__license__ = "GNU Lesser General Public License"
__package__ = "lastfm.mixins"

try:
    from threading import Lock
except ImportError:
    from dummy_threading import Lock
    
class Cacheable(object):
    registry = {}
    _lock = Lock()

    def __new__(cls, *args, **kwds):
        subject = None
        if 'subject' in kwds and not cls.__name__.startswith('Weekly'):
            subject = kwds['subject']
            #del kwds['subject']

        if 'bypass_registry' in kwds:
            del kwds['bypass_registry']
            inst = object.__new__(cls)
            inst.init(*args, **kwds)
            return inst

        key = cls._hash_func(*args, **kwds)
        if subject is not None:
            key = (hash(subject), key)

        Cacheable._lock.acquire()
        try:
            inst, already_registered = Cacheable.register(object.__new__(cls), key)
            if not already_registered:
                inst.init(*args, **kwds)
        finally:
            Cacheable._lock.release()
        return inst

    @staticmethod
    def register(ob, key):
        if not ob.__class__ in Cacheable.registry:
            Cacheable.registry[ob.__class__] = {}
        if key in Cacheable.registry[ob.__class__]:
            ob = Cacheable.registry[ob.__class__][key]
            #print "already registered: %s" % repr(ob)
            return (ob, True)
        else:
            #print "not already registered: %s" % ob.__class__
            Cacheable.registry[ob.__class__][key] = ob
            return (ob, False)
        
    @staticmethod
    def _hash_func(*args, **kwds):
        raise NotImplementedError("The subclass must override this method")
