#!/usr/bin/env python3

from distutils.core import setup

setup(name='simplebdd',
      version='0.1',
      description='Simple Behaviour Driven Development Framework',
      author='Brendan Molloy',
      author_email='brendan@bbqsrc.net',
      url='http://brendan.so/projects/simplebdd',
      download_url='https://github.com/bbqsrc/simplebdd',
      license="CC0",
      packages=['simplebdd'],
      scripts=['scripts/simplebdd'],
      classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Testing',
        'License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication',
        'License :: Public Domain'
      ]
     )
