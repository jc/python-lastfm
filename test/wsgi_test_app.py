from urlparse import urlunparse
import md5
import os
"""
A simple WSGI application for testing.
"""

_app_was_hit = False

def success():
    return _app_was_hit

def test_app(environ, start_response):
    """Simplest possible application object"""
    url =  urlunparse((
                       environ['wsgi.url_scheme'],
                       environ['HTTP_HOST'],
                       environ['PATH_INFO'],
                       '',
                       environ['QUERY_STRING'],
                       ''
                       ))
    #print "intercepted: %s" % url
    key = md5.new(url).hexdigest()
    status = '200 OK'
    response_headers = [('Content-type','text/xml')]
    start_response(status, response_headers)

    global _app_was_hit
    _app_was_hit = True
    
    filedata = unicode(open(os.path.join(os.path.dirname(__file__), 'data', key)).read())
    return [filedata]

def create_wsgi_app():
    global _app_was_hit
    _app_was_hit = False
    return test_app

if __name__ == "__main__":
    from wsgi_intercept.urllib2_intercept import install_opener
    install_opener()
    import wsgi_intercept
    wsgi_intercept.add_wsgi_intercept('ws.audioscrobbler.com', 80, create_wsgi_app)
    import urllib2
    print urllib2.urlopen('http://ws.audioscrobbler.com/2.0/?album=Supersonic&api_key=152a230561e72192b8b0f3e42362c6ff&artist=Oasis&method=album.getInfo').read()