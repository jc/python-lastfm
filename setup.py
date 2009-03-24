#!/usr/bin/env python

__author__ = "Abhinav Sarkar <abhinav@abhinavsarkar.net>"
__version__ = "0.2"
__license__ = "GNU Lesser General Public License"

METADATA = dict(
	name='lastfm',
	version='0.2',
	description="a pure python interface to the Last.fm Webservices API",
	long_description="""a pure python interface to the Last.fm Webservices API version 2.0,
located at http://ws.audioscrobbler.com/2.0/ .""",
	author="Abhinav Sarkar",
	author_email="abhinav.sarkar@gmail.com",
	maintainer="Abhinav Sarkar",
	maintainer_email="abhinav.sarkar@gmail.com",
	url="http://python-lastfm.googlecode.com/svn/trunk/dist/",
	packages=['lastfm'],
    package_data = {'doc':['*.txt', '*.htm', '*.css', '*.js', '*.png']},
	license="GNU Lesser General Public License",
	keywords="audioscrobbler webservice api last.fm",
)

SETUPTOOLS_METADATA = dict(
	install_requires = ['setuptools', 'decorator'],
	include_package_data = True,
    tests_require = ['wsgi_intercept'],
	classifiers = [
		'Development Status :: 3 - Alpha',
		'Intended Audience :: Developers',
		'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
		'Operating System :: OS Independent',
		'Programming Language :: Python',
		'Topic :: Software Development :: Libraries :: Python Modules',
		'Topic :: Multimedia :: Sound/Audio',
		'Topic :: Internet',
	],
	test_suite = "test",
)

import sys
if sys.version < '2.5':
    SETUPTOOLS_METADATA['install_requires'].append('ElementTree')
    SETUPTOOLS_METADATA['install_requires'].append('cElementTree')

def Main():
    # Use setuptools if available, otherwise fallback and use distutils
    try:
        import setuptools
        METADATA.update(SETUPTOOLS_METADATA)
        setuptools.setup(**METADATA)
    except ImportError:
        import distutils.core
        distutils.core.setup(**METADATA)

if __name__ == '__main__':
    Main()
