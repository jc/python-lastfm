import os

try:
    api_key = os.environ['LASTFM_APIKEY']
except KeyError:
    api_key = '1234' # was: '152a230561e72192b8b0f3e42362c6ff'