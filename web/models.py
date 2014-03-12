#! /usr/bin/env python
# -*- coding: utf-8 -*-

from web import db

class User(db.Model):

    id = db.Column(db.Integer, primary_key = True)
    firstname = db.Column(db.String(64), unique = True)
    lastname = db.Column(db.String(64), unique = True)
    email = db.Column(db.String(120), index = True, unique = True)
    stations = db.relationship('Station', backref = 'owner', lazy = 'dynamic')

    def __repr__(self):
        return '<User %r>' % (self.firstname)

class Station(db.Model):

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64))
    altitude = db.Column(db.Float())
    latitude = db.Column(db.Float())
    longitude = db.Column(db.Float())
    mesures = db.relationship('Mesure', backref = 'station', lazy = 'dynamic')
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    #owner = db.relationship("User", backref=db.backref('stations', order_by=id))

    def __repr__(self):
        return '<Station %r>' % (self.name)
    
class Mesure(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    temperature = db.Column(db.Float())
    pression = db.Column(db.Float())
    humidity = db.Column(db.Float())
    
    station_id = db.Column(db.Integer, db.ForeignKey('station.id'))

