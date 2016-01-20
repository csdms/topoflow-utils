#! /usr/bin/env python
from ez_setup import use_setuptools
use_setuptools()
from setuptools import setup, find_packages


setup(name='topoflow-utils',
      version='0.1.0',
      author='Mark Piper',
      author_email='mark.piper@colorado.edu',
      description='Library routines for using TopoFlow in WMT',
      long_description=open('README.md').read(),
      packages=find_packages(),
)
