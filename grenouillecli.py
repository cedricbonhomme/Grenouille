#! /usr/bin/env python
# -*- coding: utf-8 -*-

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
    parser = argparse.ArgumentParser(description='Example of Grenouille client.')
    parser.add_argument('-u','--url', dest="url",
                        default="https://petite-grenouille.herokuapp.com/weather.json/",
                        help='URL of the platform')
    parser.add_argument('-e','--email', dest="email",
                        help='Your email')
    parser.add_argument('-p','--password', dest="password",
                        help='Your password')
    parser.add_argument('-k','--api-key', dest="key",
                        help='Your API key')
    parser.add_argument('-s','--station', dest="station", type=int,
                        help='Id of the station')

    parser.add_argument('--temperature', dest="temperature", type=float,
                        default=24.5, help='Temperature')
    parser.add_argument('--pression', dest="pression", type=float,
                        default=1024, help='Pression')
    parser.add_argument('--humidity', dest="humidity", type=float,
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
