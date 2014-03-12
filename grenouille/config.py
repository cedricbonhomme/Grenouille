#! /usr/bin/env python
# -*- coding: utf-8 -*-


import os
basedir = os.path.abspath(os.path.dirname(__file__))

CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'


SQLALCHEMY_DATABASE_URI = os.environ['SQLALCHEMY_DATABASE_URI']

# slow database query threshold (in seconds)
DATABASE_QUERY_TIMEOUT = 0.5