#! /usr/bin/env python
# -*- coding: utf-8 -*-

from web.config import SQLALCHEMY_DATABASE_URI
from web import db

db.create_all()