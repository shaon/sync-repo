#!/usr/bin/env python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
import syncrepo

setup(name="sync-repo",
      version=syncrepo.__version__,
      description="",
      author="Imran Hossain",
      author_email="imran.hossain@hp.com",
      install_requires=['argparse'],
      packages=["syncrepo"],
      license='BSD (Simplified)',
      platforms='Posix; MacOS X; Windows',
      classifiers=['Development Status :: 1 - Alpha',
                   'Intended Audience :: System Administrators',
                   'License :: OSI Approved :: BSD License',
                   'Operating System :: OS Independent',
                   'Topic :: System :: Systems Administration'],
      )
