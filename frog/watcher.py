from datetime import datetime
import argparse
import sys

from yoctopuce.yocto_api import YAPI

from grenouille.station import Station
from grenouille.database import WeatherDatabase
from grenouille import logger, __version__


def watch_station(delay=3600, verbose=True, loop=False):
    delay = delay * 1000
    station = Station()
    db = WeatherDatabase()

    def _get_data():
        data = {'date': datetime.now()}
        for sensor, value, fmt_value in station.get_info():
            data[sensor.split('.')[-1]] = value

        if verbose:
            print data
        db.index(data)

    if not loop:
        _get_data()
        return

    while True:
        _get_data()
        YAPI.Sleep(delay)


def main():
    parser = argparse.ArgumentParser(description='Frog watcher.')

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
        print('Frog v%s - Yoctopuce v%s' % (__version__, yocto))
        sys.exit(0)

    try:
        watch_station(loop=args.loop, delay=args.delay, verbose=args.verbose)
    except KeyboardInterrupt:
        pass

    logger.info('Bye!')


if __name__ == '__main__':
    main()
