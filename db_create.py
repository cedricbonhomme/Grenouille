#! /usr/bin/env python
# -*- coding: utf-8 -*-

from web.config import SQLALCHEMY_DATABASE_URI
from web import db
from web.models import User, Station


db.drop_all()
db.create_all()

user = User(firstname="Cédric", lastname="Bonhomme", email="kimble.mandel@gmail.com")
station1 = Station(name="Station Apach", altitude=200, latitude=49.4594444444, longitude=6.37555555556, user_id=user.id)
station2 = Station(name="Station Luxembourg", altitude=300, latitude=49.6286904, longitude=6.1626319, user_id=user.id)
user.stations.extend([station1, station2])


db.session.add(user)
db.session.commit()