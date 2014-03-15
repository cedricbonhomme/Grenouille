#! /usr/bin/env python
# -*- coding: utf-8 -*-

from flask import jsonify
from web import app
from web.models import User, Station

@app.route('/users.json/', methods=['GET'])
def users_json():
    """
    This JSON service returns the list of all stations sorted by users.
    """
    users = User.query.all()
    result = []
    for user in users:
        dic = {
                "user" : user.id,
                "stations": [ {"name":station.name,
                               "altitude":station.altitude,
                               "latitude":station.latitude,
                               "longitude":station.longitude} for station in user.stations]
            }
        result.append(dic)
    return jsonify(result=result)

@app.route('/stations.json/', methods=['GET'])
def stations_json():
    """
    This JSON service returns the list of all stations.
    """
    users = User.query.all()
    result = []
    for user in users:
        result.extend([{"id":station.id,
                        "name":station.name,
                        "altitude":station.altitude,
                        "latitude":station.latitude,
                        "longitude":station.longitude} for station in user.stations])
    return jsonify(result=result)