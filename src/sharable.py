#!/usr/bin/env python

__author__ = "Abhinav Sarkar <abhinav@abhinavsarkar.net>"
__version__ = "0.2"
__license__ = "GNU Lesser General Public License"

class Sharable(object):
    def init(self, api):
        self.__api = api
        
    def share(self, recipient, message = None):
        from user import User
        params = self._default_params({'method': '%s.share' % self.__class__.__name__.lower()})
        if message is not None:
            params['message'] = message
        
        if not isinstance(recipient, list):
            recipient = [recipient]
            
        for i in xrange(len(recipient)):
            if isinstance(recipient[i], User):
                recipient[i] = recipient[i].name
        params['recipient'] = ",".join(recipient)
        self.__api._post_data(params)