#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

import config

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
db = SQLAlchemy(app)

from web import views, models 
