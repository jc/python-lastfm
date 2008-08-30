#!/usr/bin/env python

__author__ = "Abhinav Sarkar <abhinav@abhinavsarkar.net>"
__version__ = "0.1"
__license__ = "GNU Lesser General Public License"

class LastfmError(Exception):
	"""Base class for Lastfm errors"""
	def __init__(self,				 
				 message = None,
				 code = None):
		self.__code = code
		self.__message = message

	@property
	def code(self):
		return self.__code

	@property
	def message(self):
		return self.__message
	
	def __str__(self):
		return "%s" % self.message

class LastfmInvalidServiceError(LastfmError):#2
	pass

class LastfmInvalidMethodError(LastfmError):#3
	pass

class LastfmAuthenticationFailedError(LastfmError):#4
	pass

class LastfmInvalidFormatError(LastfmError):#5
	pass

class LastfmInvalidParametersError(LastfmError):#6
	pass

class LastfmInvalidResourceError(LastfmError):#7
	pass

class LastfmOperationFailedError(LastfmError):#8
	pass

class LastfmInvalidSessionKeyError(LastfmError):#9
	pass

class LastfmInvalidApiKeyError(LastfmError):#10
	pass

class LastfmServiceOfflineError(LastfmError):#11
	pass

class LastfmSubscribersOnlyError(LastfmError):#12
	pass

class LastfmTokenNotAuthorizedError(LastfmError):#14
	pass

class LastfmTokenExpiredError(LastfmError):#15
	pass

errorMap = {
		    1: LastfmError,
			2: LastfmInvalidServiceError,
			3: LastfmInvalidMethodError,
			4: LastfmAuthenticationFailedError,
			5: LastfmInvalidFormatError,
			6: LastfmInvalidParametersError,
			7: LastfmInvalidResourceError,
			8: LastfmOperationFailedError,
			9: LastfmInvalidSessionKeyError,
			10: LastfmInvalidApiKeyError,
			11: LastfmServiceOfflineError,
			12: LastfmSubscribersOnlyError,
			14: LastfmTokenNotAuthorizedError,
			15: LastfmTokenExpiredError
		   }	