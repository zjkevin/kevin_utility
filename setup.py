import os
import codecs
from setuptools import setup, find_packages

setup(
    name = 'kevin_utils', 
    version = '0.0.1', 
    description = u'Python3.4.4 utility lib',
    # package_dir = {'': 'syntools'},
    packages = find_packages(exclude=['tests']),
    #install_requires = ['thrift==0.9.1', 'requests>=1.2.3', 'kazoo==1.2.1', 'happybase==0.9'],
)
