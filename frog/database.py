#! /usr/bin/env python
#-*- coding: utf-8 -*-

__author__ = "Cedric Bonhomme"
__date__ = "$Date: 2013/07/01 $"
__revision__ = "$Date: 2013/07/01 $"
__copyright__ = "Copyright (c) Cedric Bonhomme"
__license__ = "GPLv3"

import json
from pyelasticsearch import ElasticSearch


class WeatherDatabase(object):

    def __init__(self, server='http://0.0.0.0:9901'):
        self.server = server
        self.es = ElasticSearch(server)

    def index(self, data):
        return self.es.index('weather', 'sensor', data)
