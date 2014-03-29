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

CSRF_ENABLED = True

SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']

# slow database query threshold (in seconds)
DATABASE_QUERY_TIMEOUT = 0.5