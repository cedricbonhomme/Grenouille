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
__date__ = "$Date: 2014/03/16 $"
__revision__ = "$Date: 2014/03/16 $"
__copyright__ = "Copyright (c) Cedric Bonhomme"
__license__ = "AGPLv3"

import os

basedir = os.path.abspath(os.path.dirname(__file__))
PATH = os.path.abspath(".")

CSRF_ENABLED = True

# slow database query threshold (in seconds)
DATABASE_QUERY_TIMEOUT = 0.5

ON_HEROKU = int(os.environ.get("HEROKU", 0)) == 1

if not ON_HEROKU:
    try:
        import configparser as confparser
    except:
        import ConfigParser as confparser
    # load the configuration
    config = confparser.SafeConfigParser()
    config.read("./conf/conf.cfg")

    PLATFORM_URL = config.get("misc", "platform_url")
    ADMIN_PLATFORM_EMAIL = config.get("misc", "admin_platform_email")
    RECAPTCHA_PUBLIC_KEY = config.get("misc", "recaptcha_public_key")
    RECAPTCHA_PRIVATE_KEY = config.get("misc", "recaptcha_private_key")

    SQLALCHEMY_DATABASE_URI = config.get("database", "uri")

    WEBSERVER_DEBUG = int(config.get("webserver", "debug")) == 1
    WEBSERVER_HOST = config.get("webserver", "host")
    WEBSERVER_PORT = int(config.get("webserver", "port"))

else:
    PLATFORM_URL = os.environ.get("PLATFORM_URL", "https://pyaggr3g470r.herokuapp.com/")
    ADMIN_PLATFORM_EMAIL = os.environ.get("ADMIN_PLATFORM_EMAIL", "")
    RECAPTCHA_PUBLIC_KEY = os.environ.get("RECAPTCHA_PUBLIC_KEY", "")
    RECAPTCHA_PRIVATE_KEY = os.environ.get("RECAPTCHA_PRIVATE_KEY", "")

    SQLALCHEMY_DATABASE_URI = os.environ["DATABASE_URL"]
