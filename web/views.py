#! /usr/bin/env python
# -*- coding: utf-8 -*-

from flask import render_template, jsonify, request

from web import app, db
from web.models import User, Station




@app.route('/users.json/', methods=['GET'])
def users_json():
    """
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

@app.route('/map/', methods=['GET'])
def map_view():
    """
    """
    #users = User.query.all()
    return render_template('map.html')