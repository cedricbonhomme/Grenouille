#! /usr/bin/env python
#-*- coding: utf-8 -*-

import json


class WeatherDatabase(object):

    def __init__(self, server='http://0.0.0.0:9901'):
        self.server = server

    def index(self, data):
        return self.es.index('weather', 'sensor', data)
