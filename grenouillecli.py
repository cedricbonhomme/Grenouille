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
__version__ = "$Revision: 0.1 $"
__date__ = "$Date: 2014/03/26 $"
__revision__ = "$Date: 2014/03/26 $"
__copyright__ = "Copyright (c) Cedric Bonhomme"
__license__ = "AGPLv3"

import json
import requests

def send_measure(url, data, email, password):
    """
    Send a measure to the Grenouille platform.
    """
    headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
    r = requests.post(url, data=json.dumps(data), headers=headers, auth=(email, password))
    if r.status_code == 200:
        print(r.content)
    else:
        print(r.status_code)

if __name__ == "__main__":
    # Point of entry in execution mode
    import argparse
    parser = argparse.ArgumentParser(description='Client to send weather data to the Grenouille platform.')
    parser.add_argument('--url', dest="url",
                        default="https://petite-grenouille.herokuapp.com/weather.json/",
                        help='URL of the platform')
    parser.add_argument('--email', dest="email", required=True,
                        help='Your email')
    parser.add_argument('--password', dest="password", required=True,
                        help='Your password')
    parser.add_argument('--api-key', dest="key", required=True,
                        help='Your API key')
    parser.add_argument('--station', dest="station", type=int, required=True,
                        help='Id of the station')

    parser.add_argument('--temperature', dest="temperature", type=float, required=True,
                        default=24.5, help='Temperature')
    parser.add_argument('--pression', dest="pression", type=float, required=True,
                        default=1024, help='Pression')
    parser.add_argument('--humidity', dest="humidity", type=float, required=True,
                        default=52, help='Humidity')

    args = parser.parse_args()

    data = {
            'api_key': args.key, \
            'station_id': args.station, \
            'pression': args.pression, \
            'temperature': args.temperature, \
            'humidity': args.humidity \
           }

    send_measure(args.url, data, args.email, args.password)
