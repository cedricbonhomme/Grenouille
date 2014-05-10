#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Grenouille - An online service for weather data.
# Copyright (C) 2014 Cédric Bonhomme - http://cedricbonhomme.org/
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

__author__ = "Cedric Bonhomme"
__version__ = "$Revision: 0.3 $"
__date__ = "$Date: 2014/03/16 $"
__revision__ = "$Date: 2014/04/05 $"
__copyright__ = "Copyright (c) Cedric Bonhomme"
__license__ = "AGPLv3"

import re
import json
import random, base64, hashlib
from datetime import datetime
from werkzeug import generate_password_hash, check_password_hash
from flask.ext.login import UserMixin
from web import db

class User(db.Model, UserMixin):
    """
    Represent a user.
    """
    id = db.Column(db.Integer, primary_key = True)
    firstname = db.Column(db.String(64))
    lastname = db.Column(db.String(64))
    email = db.Column(db.String(120), index = True, unique = True)
    pwdhash = db.Column(db.String(120))
    roles = db.relationship('Role', backref = 'user', lazy = 'dynamic')
    date_created = db.Column(db.DateTime(), default=datetime.now)
    last_seen = db.Column(db.DateTime(), default=datetime.now)
    apikey = db.Column(db.String(86), default = base64.b64encode(hashlib.sha512( str(random.getrandbits(256)) ).digest(),
                                                                                random.choice(['rA','aZ','gQ','hH','hG','aR','DD'])).rstrip('=='))
    stations = db.relationship('Station', backref = 'owner', lazy = 'dynamic', cascade='all,delete-orphan')

    @staticmethod
    def make_valid_nickname(nickname):
        return re.sub(ur'[^\w \-]', '', nickname, flags=re.U)

    def get_id(self):
        """
        Return the id (email) of the user.
        """
        return self.email

    def set_password(self, password):
        """
        Hash the password of the user.
        """
        self.pwdhash = generate_password_hash(password)

    def check_password(self, password):
        """
        Check the password of the user.
        """
        return check_password_hash(self.pwdhash, password)

    def is_admin(self):
        """
        Return True if the user has administrator rights.
        """
        return len([role for role in self.roles if role.name == "admin"]) != 0

    def __eq__(self, other):
        return self.id == other.id

    def __repr__(self):
        return '<User %r>' % (self.firstname)

class Role(db.Model):
    """
    Represent a role.
    """
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(10), unique = True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Station(db.Model):
    """
    Represent a station.
    """
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64), default="New station")
    country = db.Column(db.String(64), default="FR")
    altitude = db.Column(db.Float())
    latitude = db.Column(db.Float())
    longitude = db.Column(db.Float())
    measures = db.relationship('Measure', backref = 'station', lazy = 'dynamic', cascade='all,delete-orphan')

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Station %r>' % (self.name)

class Measure(db.Model):
    """
    Represent a measure from a station.
    Units of measure:
    - temperature: °C;
    - pression: hpa;
    - humidity: percent;
    - wind: m/s.
    """
    id = db.Column(db.Integer, primary_key = True)
    temperature = db.Column(db.Float())
    pression = db.Column(db.Float())
    humidity = db.Column(db.Float())
    wind = db.Column(db.Float())
    date = db.Column(db.DateTime(), default=datetime.now)

    station_id = db.Column(db.Integer, db.ForeignKey('station.id'))

    def __repr__(self):
        return json.dumps({"temperature": self.temperature,
                "pression": self.pression,
                "humidity": self.humidity,
                "date": str(self.date)})
