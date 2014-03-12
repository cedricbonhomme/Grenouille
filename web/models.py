#! /usr/bin/env python
# -*- coding: utf-8 -*-

from web import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    firstname = db.Column(db.String(64), unique = True)
    lastname = db.Column(db.String(64), unique = True)
    email = db.Column(db.String(120), index = True, unique = True)
    stations = db.relationship('Station', backref = 'owner', lazy = 'dynamic')
    
    def __init__(self, firstname, lastname, email):
        self.firstname = firstname
        self.lastname = lastname
        self.email = email

    def __repr__(self):
        return '<User %r>' % (self.firstname)

class Station(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64))
    altitude = db.Column(db.Float())
    latitude = db.Column(db.Float())
    longitude = db.Column(db.Float())
    mesures = db.relationship('Mesure', backref = 'station', lazy = 'dynamic')

    def __init__(self, name, altitude, longitude, latitude):
        self.name = name
        self.altitude = altitude
        self.longitude = longitude
        self.latitude = latitude

    def __repr__(self):
        return '<Station %r>' % (self.name)
    
class Mesure(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    temperature = db.Column(db.Float())
    pression = db.Column(db.Float())
    humidity = db.Column(db.Float())

    def __init__(self, temperature, pression, humidity):
        self.temperature = temperature
        self.pression = pression
        self.humidity = humidity