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
__version__ = "$Revision: 0.2 $"
__date__ = "$Date: 2014/03/16 $"
__revision__ = "$Date: 2014/03/24 $"
__copyright__ = "Copyright (c) Cedric Bonhomme"
__license__ = "AGPLv3"

from flask import flash
from flask.ext.wtf import Form
from wtforms import TextField, TextAreaField, SelectField, PasswordField, SubmitField, validators

from web.models import User

import logging
logging.getLogger('pycountry').addHandler(logging.NullHandler())
import pycountry

class SigninForm(Form):
    """
    Sign in form.
    """
    email = TextField("Email", [validators.Required("Please enter your email address."), validators.Email("Please enter your email address.")])
    password = PasswordField('Password', [validators.Required("Please enter a password.")])
    submit = SubmitField("Log In")

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

    def validate(self):
        if not Form.validate(self):
            return False

        user = User.query.filter(User.email == self.email.data).first()
        if user and user.check_password(self.password.data):
            return True
        else:
            flash('Invalid email or password', 'danger')
            #self.email.errors.append("Invalid email or password")
            return False

class ProfileForm(Form):
    """
    Profile form.
    """
    firstname = TextField("First name", [validators.Required("Please enter your first name.")])
    lastname = TextField("Last name", [validators.Required("Please enter your last name.")])
    email = TextField("Email", [validators.Required("Please enter your email.")])
    password = PasswordField("Password")
    submit = SubmitField("Save")

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

    def validate(self):
        if not Form.validate(self):
            return False
        return True

class StationForm(Form):
    """
    Station form.
    """
    name = TextField("Name", [validators.Required("Please enter a name.")])
    country = SelectField(u'Country', choices=[(country.alpha2, country.name) for country in  list(pycountry.countries)])
    altitude = TextField("Altitude", [validators.Required("Please enter an altitude.")])
    latitude = TextField("Latitude", [validators.Required("Please enter a latitude.")])
    longitude = TextField("Longitude", [validators.Required("Please enter a longitude.")])
    submit = SubmitField("Save")

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

    def validate(self):
        if not Form.validate(self):
            return False
        return True