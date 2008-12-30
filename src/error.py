#!/usr/bin/env python

__author__ = "Abhinav Sarkar <abhinav@abhinavsarkar.net>"
__version__ = "0.2"
__license__ = "GNU Lesser General Public License"

class LastfmError(Exception):
    """Base class for Lastfm errors"""
    def __init__(self,                 
                 message = None,
                 code = None):
        super(LastfmError, self).__init__()
        self._code = code
        self._message = message

    @property
    def code(self):
        return self._code

    @property
    def message(self):
        return self._message
    
    def __str__(self):
        return "%s" % self.message

class InvalidServiceError(LastfmError):#2
    pass

class InvalidMethodError(LastfmError):#3
    pass

class AuthenticationFailedError(LastfmError):#4
    pass

class InvalidFormatError(LastfmError):#5
    pass

class InvalidParametersError(LastfmError):#6
    pass

class InvalidResourceError(LastfmError):#7
    pass

class OperationFailedError(LastfmError):#8
    pass

class InvalidSessionKeyError(LastfmError):#9
    pass

class InvalidApiKeyError(LastfmError):#10
    pass

class ServiceOfflineError(LastfmError):#11
    pass

class SubscribersOnlyError(LastfmError):#12
    pass

class TokenNotAuthorizedError(LastfmError):#14
    pass

class TokenExpiredError(LastfmError):#15
    pass

error_map = {
            1: LastfmError,
            2: InvalidServiceError,
            3: InvalidMethodError,
            4: AuthenticationFailedError,
            5: InvalidFormatError,
            6: InvalidParametersError,
            7: InvalidResourceError,
            8: OperationFailedError,
            9: InvalidSessionKeyError,
            10: InvalidApiKeyError,
            11: ServiceOfflineError,
            12: SubscribersOnlyError,
            14: TokenNotAuthorizedError,
            15: TokenExpiredError
           }    