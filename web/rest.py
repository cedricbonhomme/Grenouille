#! /usr/bin/env python
# -*- coding: utf-8 -*-

from flask import g, jsonify, request
from flask.ext.login import login_required
from web import app, db
from web.models import User, Station, Mesure

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
        for station in user.stations:
            try:
                last_measure_date = station.mesures[-1].date
                last_measure_temperature = station.mesures[-1].temperature
                last_measure_pression = station.mesures[-1].pression
                last_measure_humidity = station.mesures[-1].humidity
            except:
                last_measure_date = ""
                last_measure_temperature = ""
                last_measure_pression = ""
                last_measure_humidity = ""
            result.append({"id":station.id,
                            "name":station.name,
                            "altitude":station.altitude,
                            "latitude":station.latitude,
                            "longitude":station.longitude,
                            "date":last_measure_date,
                            "temperature":last_measure_temperature,
                            "pression":last_measure_pression,
                            "humidity":last_measure_humidity})
    return jsonify(result=result)

@app.route('/mesure.json/', methods=['POST'])
@auth.login_required
def mesure_json():
    """
    Retrieves mesures send by a station.
    """
    user = User.query.filter(User.email == g.user.email).first()
    try:
        api_key = request.json["api_key"]
        station_id = int(request.json["station_id"])
    except:
        return jsonify(result="UNAUTHORIZED")
    if user.apikey != api_key:
        return jsonify(result="UNAUTHORIZED")
    for station in user.stations:
        if station.id == station_id:
            new_mesure = Mesure(temperature=request.json["temperature"],
                                humidity=request.json["humidity"],
                                pression=request.json["pression"])
            station.mesures.append(new_mesure)
            db.session.commit()
            break
    else:
        return jsonify(result="BAD STATION ID")
    return jsonify(result="OK")