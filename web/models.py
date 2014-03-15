#! /usr/bin/env python
# -*- coding: utf-8 -*-

import random, base64, hashlib
from werkzeug import generate_password_hash, check_password_hash
from flask.ext.login import UserMixin
from web import db

class User(db.Model, UserMixin):
    """
    Represent a user.
    """
    id = db.Column(db.Integer, primary_key = True)
    firstname = db.Column(db.String(64), unique = True)
    lastname = db.Column(db.String(64), unique = True)
    email = db.Column(db.String(120), index = True, unique = True)
    pwdhash = db.Column(db.String(120), unique = True)
    apikey = db.Column(db.String(86), unique = True, default = base64.b64encode(hashlib.sha512( str(random.getrandbits(256)) ).digest(),
                                                                                random.choice(['rA','aZ','gQ','hH','hG','aR','DD'])).rstrip('=='))
    stations = db.relationship('Station', backref = 'owner', lazy = 'dynamic')

    def get_id(self):
        return self.email

    def set_password(self, password):
        self.pwdhash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pwdhash, password)

    def __repr__(self):
        return '<User %r>' % (self.firstname)

class Station(db.Model):
    """
    Represent a station.
    """
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64), default="New station")
    altitude = db.Column(db.Float())
    latitude = db.Column(db.Float())
    longitude = db.Column(db.Float())
    mesures = db.relationship('Mesure', backref = 'station', lazy = 'dynamic')

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Station %r>' % (self.name)

class Mesure(db.Model):
    """
    Represent a mesure from a station.
    """
    id = db.Column(db.Integer, primary_key = True)
    temperature = db.Column(db.Float())
    pression = db.Column(db.Float())
    humidity = db.Column(db.Float())

    station_id = db.Column(db.Integer, db.ForeignKey('station.id'))
