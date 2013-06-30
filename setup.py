# -*- encoding: utf8 -*-
import os
import sys

from setuptools import setup, find_packages
from frog import __version__


setup(name='frog',
      version=__version__,
      packages=find_packages(),
      description="Weather station",
      author="Cédric Bonhomme",
      author_email="kimble.mandel@gmail.com",
      include_package_data=True,
      install_requires=['yoctopuce', 'requests'],
       entry_points="""
      [console_scripts]
      frog = frog.watcher:main
      """,
      zip_safe=False
      )
