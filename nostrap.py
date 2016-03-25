#!/usr/bin/env python
"""
nostrap.py

Get virtualenv and other
packages from pypi with nothing but python installed.

.. codeauthor:: Jordan Speicher
"""
from __future__ import absolute_import
import sys
import os
import shutil
import tempfile
try:
    from urllib.request import urlopen
    from xmlrpc.client import ServerProxy
except ImportError:
    from urllib2 import urlopen
    from xmlrpclib import ServerProxy

HOST = 'https://pypi.python.org/pypi'

def get_package_dist(name, version='latest', packagetype='bdist_wheel'):
    """
    Get a description of a package from a pypi server.
    """
    pypi = ServerProxy(HOST)

    if version == 'latest':
        version = pypi.package_releases(name)[0]

    urls = pypi.release_urls(name, version)
    if not urls:
        print('No package "{}" version "{}"'.format(name, version))
        return None

    dists = [d for d in urls if d['packagetype'] == packagetype]
    if not dists:
        print('No package "{}" type "{}"'.format(name, packagetype))
        return None

    return dists[0]

def download_package(name, dest, **kwargs):
    """
    Download a package and return the name of the file.
    """
    dist = get_package_dist(name, **kwargs)
    if not dist:
        return None

    url = dist['url']
    filename = dist['filename']
    stream = urlopen(url)

    with open(os.path.join(dest, filename), 'w+b') as temp:
        print('Get {}'.format(filename))
        temp.write(stream.read())
        return temp.name

def require(name, dest, **kwargs):
    """
    Import and return a package by name.  If the package does not exist,
    download from pypi, import and return it.
    """
    try:
        return __import__(name, globals(), locals(), level=0)
    except ImportError:
        temp = download_package(name, dest, **kwargs)
        if not temp:
            raise Exception('Cannot download package {}'.format(name))
        sys.path.append(temp)
        return __import__(name, globals(), locals(), level=0)

if __name__ == '__main__':
    tempdir = tempfile.mkdtemp()
    try:
        require('pip', tempdir)
        sys.argv += ['--download']
        sys.argv += ['--extra-search-dir', tempdir]
        virtualenv = require('virtualenv', tempdir)
        virtualenv.main()
    finally:
        shutil.rmtree(tempdir)

