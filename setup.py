from __future__ import unicode_literals

from setuptools import setup

from readabledelta import __version__  # simple solution because we have no 3rd party dependencies

with open('README.rst') as f:
    long_description = f.read()

setup(
    name='readabledelta',
    version=__version__,
    description='Human readable modification of timedelta',
    long_description=long_description,
    author='Wim Glenn',
    author_email='hey@wimglenn.com',
    url='https://github.com/wimglenn/readabledelta',
    py_modules=['readabledelta'],
    include_package_data=True,
)
