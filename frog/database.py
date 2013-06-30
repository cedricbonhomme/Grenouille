import json
from pyelasticsearch import ElasticSearch


class WeatherDatabase(object):

    def __init__(self, server='http://0.0.0.0:9901'):
        self.server = server
        self.es = ElasticSearch(server)

    def index(self, data):
        return self.es.index('weather', 'sensor', data)
