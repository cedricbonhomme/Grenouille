#! /usr/bin/env python
# -*- coding: utf-8 -*-

from web import db
from web.models import User, Station
from werkzeug import generate_password_hash

db.drop_all()
db.create_all()

user = User(firstname="admin", lastname="admin", email="email@mail.com", pwdhash=generate_password_hash("password"))
station1 = Station(name="Metz", altitude=200, latitude=49.115558, longitude=6.175635, user_id=user.id)
station2 = Station(name="Luxembourg Kirchberg", altitude=300, latitude=49.6286904, longitude=6.1626319, user_id=user.id)
station3 = Station(name="New-York", altitude=320, latitude=40.717977, longitude=-74.006015, user_id=user.id)
user.stations.extend([station1, station2, station3])

db.session.add(user)
db.session.commit()