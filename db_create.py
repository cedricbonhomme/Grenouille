#! /usr/bin/env python
# -*- coding: utf-8 -*-

from grenouille.config import SQLALCHEMY_DATABASE_URI
from grenouille import db

db.create_all()