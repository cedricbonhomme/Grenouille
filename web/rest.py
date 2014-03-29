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
__version__ = "$Revision: 0.2 $"
__date__ = "$Date: 2014/03/16 $"
__revision__ = "$Date: 2014/03/24 $"
__copyright__ = "Copyright (c) Cedric Bonhomme"
__license__ = "AGPLv3"

from flask import g, jsonify, request
from flask.ext.login import login_required
from web import app, db
from web.models import User, Station, Measure

from flask.ext.httpauth import HTTPBasicAuth
auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(email, password):
    user = User.query.filter(User.email == email).first()
    if not user or not user.check_password(password):
        return False
    g.user = user
    return True

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
                               "coord": {
                                        "alt":station.altitude,
                                        "lat":station.latitude,
                                        "lon":station.longitude,
                                     }
                               } for station in user.stations]
            }
        result.append(dic)
    return jsonify(result=result)

@app.route('/weather.json/', methods=['GET'])
def weather():
    """
    This JSON service returns the list of all stations.
    """
    users = User.query.all()
    result = []
    for user in users:
        for station in user.stations:
            try:
                last_measure_date = station.measures[-1].date
                last_measure_temperature = station.measures[-1].temperature
                last_measure_pression = station.measures[-1].pression
                last_measure_humidity = station.measures[-1].humidity
            except:
                last_measure_date = ""
                last_measure_temperature = ""
                last_measure_pression = ""
                last_measure_humidity = ""
            result.append({
                            "id":station.id,
                            "name":station.name,
                            "date":last_measure_date,
                            "coord": {
                                        "lat":station.latitude,
                                        "lon":station.longitude,
                                     },
                            "main": {
                                        "temperature":last_measure_temperature,
                                        "pression":last_measure_pression,
                                        "humidity":last_measure_humidity
                                    }
                        })
    return jsonify(result=result)

@app.route('/weather.json/', methods=['POST'])
@auth.login_required
def measure_json():
    """
    Retrieves measures send by a station.
    """
    user = User.query.filter(User.email == g.user.email).first()
    try:
        api_key = request.json["api_key"]
        station_id = int(request.json["station_id"])
    except:
        return jsonify(result="UNAUTHORIZED")
    if user.apikey == "" or user.apikey != api_key:
        return jsonify(result="UNAUTHORIZED")
    for station in user.stations:
        if station.id == station_id:
            new_measure = Measure(temperature=request.json["temperature"],
                                humidity=request.json["humidity"],
                                pression=request.json["pression"])
            station.measures.append(new_measure)
            db.session.commit()
            break
    else:
        return jsonify(result="BAD STATION ID")
    return jsonify(result="OK")