#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
basedir = os.path.abspath(os.path.dirname(__file__))

CSRF_ENABLED = True

SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']

# slow database query threshold (in seconds)
DATABASE_QUERY_TIMEOUT = 0.5