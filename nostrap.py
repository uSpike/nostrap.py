"""
nostrap.py

Get virtualenv and other
packages from pypi with nothing but python installed.

.. codeauthor:: Jordan Speicher jordan@jspeicher.com
"""
from __future__ import absolute_import
import sys
import os
import shutil
import tempfile
import atexit
try:
    from urllib.request import urlopen
    from xmlrpc.client import ServerProxy
except ImportError:
    from urllib2 import urlopen
    from xmlrpclib import ServerProxy

HOST = 'https://pypi.python.org/pypi'

_TEMPDIR = tempfile.mkdtemp()
atexit.register(shutil.rmtree, _TEMPDIR)

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

def download_package(name, dest=_TEMPDIR, **kwargs):
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
        print('Get {} -> {}'.format(url.split('/')[-1], temp.name))
        temp.write(stream.read())
        return temp.name

def require(name, **kwargs):
    """
    Import and return a package by name.  If the package does not exist,
    download from pypi, import and return it.
    """
    try:
        return __import__(name, globals(), locals(), level=0)
    except ImportError:
        temp = download_package(name, **kwargs)
        if not temp:
            raise Exception('Cannot download package {}'.format(name))
        sys.path.append(temp)
        return __import__(name, globals(), locals(), level=0)

def make_virtualenv(vdir, **kwargs):
    """
    Wrapper around virtualenv to download dependency packages
    as needed.
    """
    if os.path.exists(vdir):
        print('vdir exists: {}'.format(vdir))
        print('Will not create new virtual env')
        return

    required = []
    if not kwargs.get('no_pip'):
        download_package('pip')

    if not kwargs.get('no_setuptools'):
        download_package('setuptools')

    if not kwargs.get('no_wheel'):
        download_package('wheel')

    search_dirs = kwargs.get('search_dirs', [])
    kwargs['search_dirs'] = [_TEMPDIR] + search_dirs

    virtualenv = require('virtualenv')
    virtualenv.create_environment(vdir, **kwargs)
    print('Created virtual env: {}'.format(vdir))

if __name__ == '__main__':
    if os.environ.get('DEBUG') == True:
        import logging
        logging.basicConfig(level=logging.DEBUG)

    vdir = 'pyenv'
    if len(sys.argv) > 1:
        vdir = sys.argv[1]
    make_virtualenv(vdir)
