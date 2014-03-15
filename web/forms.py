#! /usr/bin/env python
# -*- coding: utf-8 -*-

from flask.ext.wtf import Form
from wtforms import TextField, TextAreaField, PasswordField, SubmitField, validators

from web.models import User


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
            self.email.errors.append("Invalid e-mail or password")
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