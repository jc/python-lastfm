#!/usr/bin/env python

__author__ = "Abhinav Sarkar"
__version__ = "0.1"
__license__ = "GNU Lesser General Public License"

class LastfmBase(object):
    """Base class for all the classes in this package"""
    
    registry = {}
    
    def __new__(cls, *args, **kwds):
        if 'bypassRegistry' in kwds:
                del kwds['bypassRegistry']
                inst = object.__new__(cls)
                inst.init(*args, **kwds)
                return inst
        
        key = cls.hashFunc(*args, **kwds)        
        inst, alreadyRegistered = LastfmBase.register(object.__new__(cls), key)
        if not alreadyRegistered:
            inst.init(*args, **kwds)
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
            
    def __gt__(self, other):
        return not (self.__lt__(other) or self.__eq(other))
    
    def __ne__(self, other):
        return not self.__eq__(other)
    
    def __ge__(self, other):
        return not self.__lt__(other)
    
    def __le__(self, other):
        return not self.__gt__(other)