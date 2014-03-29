#! /usr/bin/env python
#-*- coding: utf-8 -*-

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

from datetime import datetime
import argparse
import sys

from yoctopuce.yocto_api import YAPI
from yoctometeo.station import Station
from yoctometeo import logger, __version__


def watch_station(delay=3600, verbose=True, loop=False):
    delay = delay * 1000
    station = Station()

    def _get_data():
        data = {'date': datetime.now()}
        for sensor, value, fmt_value in station.get_info():
            data[sensor.split('.')[-1]] = value

        if verbose:
            print data

    if not loop:
        _get_data()
        return

    while True:
        _get_data()
        YAPI.Sleep(delay)


def main():
    parser = argparse.ArgumentParser(description='Grenouille watcher.')

    parser.add_argument('--version', action='store_true', default=False,
                        help='Displays version and exits.')

    parser.add_argument('-d', '--delay',
                        help='Delay in seconds between two calls.',
                        type=int, default=3600.)

    parser.add_argument('-v', '--verbose', action='store_true',
                        help='Verbose', default=False)

    parser.add_argument('-l', '--loop', action='store_true',
                        help='Loop forever', default=False)

    args = parser.parse_args()

    if args.version:
        yocto = YAPI.GetAPIVersion()
        print('Grenouille v%s - Yoctopuce v%s' % (__version__, yocto))
        sys.exit(0)

    try:
        watch_station(loop=args.loop, delay=args.delay, verbose=args.verbose)
    except KeyboardInterrupt:
        pass

    logger.info('Bye!')


if __name__ == '__main__':
    main()
