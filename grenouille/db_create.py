#! /usr/bin/env python
# -*- coding: utf-8 -*-

from config import SQLALCHEMY_DATABASE_URI
from grenouille import db

db.create_all()