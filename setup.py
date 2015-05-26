from __future__ import unicode_literals

from setuptools import setup

with open('README.rst') as f:
    long_description = f.read()

setup(
    name='readabledelta',
    version='0.0.1-dev',
    description='Human readable modification of timedelta',
    long_description=long_description,
    author='Wim Glenn',
    author_email='hey@wimglenn.com',
    url='https://github.com/wimglenn/readabledelta',
    py_modules=['readabledelta'],
    include_package_data=True,
)
