#! /usr/bin/env python
# -*- coding: utf-8 -*-

import json
import requests

def send_measure(url, data, email, password):
    """
    """
    headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
    r = requests.post(url, data=json.dumps(data), headers=headers, auth=(email, password))
    if r.status_code == 200:
        print(r.content)
    else:
        print(r.status_code)

if __name__ == "__main__":
    # Point of entry in execution mode
    url = "https://petite-grenouille.herokuapp.com/weather.json/"
    data = {'pression': 1023, 'api_key': 'VDZCF0aa1nUazxbCX2q01FKRWALxdIzCMNmg', 'temperature': 20, 'station_id': 2, 'humidity': 81}

    send_measure(url, data, email, password)