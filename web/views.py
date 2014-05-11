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
__version__ = "$Revision: 0.3 $"
__date__ = "$Date: 2014/03/16 $"
__revision__ = "$Date: 2014/03/04 $"
__copyright__ = "Copyright (c) Cedric Bonhomme"
__license__ = "AGPLv3"

import json
from datetime import datetime
from flask import render_template, jsonify, request, flash, session, url_for, redirect, g, current_app, make_response
from flask.ext.login import LoginManager, login_user, logout_user, login_required, current_user, AnonymousUserMixin
from flask.ext.principal import Principal, Identity, AnonymousIdentity, identity_changed, identity_loaded, Permission, RoleNeed, UserNeed
from sqlalchemy.exc import IntegrityError

from web import app, db
from web.models import User, Station, Role
from forms import SignupForm, SigninForm, ProfileForm, StationForm
from werkzeug import generate_password_hash

import logging
logging.getLogger('pycountry').addHandler(logging.NullHandler())
import pycountry

Principal(app)
# Create a permission with a single Need, in this case a RoleNeed.
admin_permission = Permission(RoleNeed('admin'))

login_manager = LoginManager()
login_manager.init_app(app)

#
# Management of the user's session.
#
@identity_loaded.connect_via(app)
def on_identity_loaded(sender, identity):
    # Set the identity user object
    identity.user = current_user

    # Add the UserNeed to the identity
    if hasattr(current_user, 'id'):
        identity.provides.add(UserNeed(current_user.id))

    # Assuming the User model has a list of roles, update the
    # identity with the roles that the user provides
    if hasattr(current_user, 'roles'):
        for role in current_user.roles:
            identity.provides.add(RoleNeed(role.name))

@app.before_request
def before_request():
    g.user = current_user
    if g.user.is_authenticated():
        g.user.last_seen = datetime.utcnow()
        db.session.add(g.user)
        db.session.commit()

#
# Custom error pages.
#
@app.errorhandler(401)
def authentication_required(e):
    flash('Authentication required.', 'info')
    return redirect(url_for('login'))

@app.errorhandler(403)
def authentication_failed(e):
    flash('Forbidden.', 'danger')
    return redirect(url_for('login'))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('errors/500.html'), 500

@login_manager.user_loader
def load_user(email):
    # Return an instance of the User model
    return User.query.filter(User.email == email).first()

def redirect_url(default='map_view'):
    return request.args.get('next') or \
            request.referrer or \
            url_for(default)


#
# Views.
#
@app.route('/login/', methods=['GET', 'POST'])
def login():
    """
    Log in view.
    """
    g.user = AnonymousUserMixin()
    form = SigninForm()

    if form.validate_on_submit():
        user = User.query.filter(User.email == form.email.data).first()
        login_user(user)
        g.user = user
        identity_changed.send(current_app._get_current_object(), identity=Identity(user.id))
        flash("Logged in successfully.", 'success')
        return redirect(url_for('profile'))
    return render_template('login.html', form=form)

@app.route('/logout/')
@login_required
def logout():
    """
    Log out view. Removes the user information from the session.
    """
    # Update last_seen field
    g.user.last_seen = datetime.utcnow()
    db.session.add(g.user)
    db.session.commit()

    # Remove the user information from the session
    logout_user()

    # Remove session keys set by Flask-Principal
    for key in ('identity.name', 'identity.auth_type'):
        session.pop(key, None)

    # Tell Flask-Principal the user is anonymous
    identity_changed.send(current_app._get_current_object(), identity=AnonymousIdentity())

    flash("Logged out successfully.", 'success')
    return redirect(url_for('map_view'))

@app.route('/signup/', methods=['GET', 'POST'])
def signup():
    """
    Signup page.
    """
    form = SignupForm()

    if form.validate_on_submit():
        role_user = Role.query.filter(Role.name == "user").first()
        user = User(firstname=form.firstname.data,
                    lastname=form.lastname.data,
                    email=form.email.data,
                    pwdhash=generate_password_hash(form.password.data))
        user.roles = [role_user]
        db.session.add(user)
        try:
            db.session.commit()
        except IntegrityError:
            flash('Email already used.', 'warning')
            return render_template('signup.html', form=form)

        flash('Your account has been created. You can now sign in.', 'success')
        return redirect(url_for('login'))

    return render_template('signup.html', form=form)

@app.route('/', methods=['GET'])
def map_view():
    """
    Main view which displays all public stations.
    """
    return render_template('map.html')

@app.route('/profile/', methods=['GET', 'POST'])
@login_required
def profile():
    """
    Edit the profile of the currently logged user.
    """
    user = User.query.filter(User.email == g.user.email).first()
    form = ProfileForm()

    if request.method == 'POST':
        if form.validate():
            form.populate_obj(user)
            if form.password.data != "":
                user.set_password(form.password.data)
            db.session.commit()
            flash('User "' + user.firstname + '" successfully updated.', 'success')
            return redirect(url_for('profile'))
        else:
            return render_template('profile.html', form=form)

    if request.method == 'GET':
        form = ProfileForm(obj=user)
        return render_template('profile.html', user=user, form=form)

@app.route('/station/<int:station_id>/', methods=['GET'])
def station(station_id=None):
    """
    Edit the information about a station.
    """
    station = Station.query.filter(Station.id == station_id).first()
    country = pycountry.countries.get(alpha2=station.country).official_name
    return render_template('station.html', station=station, country=country)

@app.route('/create_station/', methods=['GET', 'POST'])
@app.route('/edit_station/<int:station_id>/', methods=['GET', 'POST'])
@login_required
def edit_station(station_id=None):
    """
    Add or edit a station.
    """
    user = User.query.filter(User.email == g.user.email).first()
    form = StationForm()

    if station_id != None:
        station = None
        for station in user.stations:
            if station.id == station_id:
                station = station
                break
        else:
            flash('This station does not exist.', 'danger')
            return redirect(redirect_url())

    if request.method == 'POST':
        if form.validate():
            if station_id != None:
                # Edit a station
                form.populate_obj(station)
                flash('Station "' + station.name + '" successfully updated.', 'success')
            else:
                # Create a new station
                station = Station(name=form.name.data,
                                    country=form.country.data,
                                    altitude=form.altitude.data,
                                    latitude=form.latitude.data,
                                    longitude=form.longitude.data,
                                    user_id=user.id)
                user.stations.append(station)
                flash('Station "' + station.name + '" successfully created.', 'success')
            db.session.commit()
        else:
            flash('Problem with the form.', 'danger')
            return redirect(redirect_url())
        return redirect("/edit_station/"+str(station.id)+"/")

    if request.method == 'GET':
        if station_id != None:
            form = StationForm(obj=station)
            message = "Edit the station <i>" + station.name + "</i>"
        else:
            form = StationForm()
            message="Add a new station"
        return render_template('edit_station.html', user=user, form=form, message=message)

@app.route('/delete_station/<int:station_id>/', methods=['GET'])
@login_required
def delete_station(station_id=None):
    """
    Delete a station.
    """
    user = User.query.filter(User.email == g.user.email).first()
    for station in user.stations:
        if station.id == station_id:
            db.session.delete(station)
            db.session.commit()
            flash('Station "' + station.name + '" successfully deleted.', 'success')
            break
    else:
        flash('This station does not exist.', 'danger')
    return redirect(redirect_url())

@app.route('/download_station/<int:station_id>/', methods=['GET'])
@login_required
def download_station(station_id):
    """
    Return all measures sent by a station in a JSON file.
    """
    user = User.query.filter(User.email == g.user.email).first()
    measures = []
    for station in user.stations:
        if station.id == station_id:
            measures.extend([json.loads(str(measure)) for measure in station.measures])
            break
    r = make_response( jsonify(measures=measures) )
    r.mimetype = 'application/json'
    r.headers["Content-Disposition"] = 'attachment; filename=measures_station_'+str(station.id)+'.json'
    return r

@app.route('/delete_account/', methods=['GET'])
@login_required
def delete_account():
    """
    Delete the account of the user (with all its data).
    """
    user = User.query.filter(User.email == g.user.email).first()
    if user is not None:
        db.session.delete(user)
        db.session.commit()
        flash('Your account has been deleted.', 'success')
    else:
        flash('This user does not exist.', 'danger')
    return redirect(url_for('login'))

@app.route('/about/', methods=['GET'])
def about():
    """
    'About' page.
    """
    return render_template('about.html')

#
# Views dedicated to administration tasks.
#
@app.route('/admin/dashboard/', methods=['GET', 'POST'])
@login_required
@admin_permission.require()
def dashboard():
    """
    Adminstrator's dashboard.
    """
    users = User.query.all()
    users.remove(g.user)
    return render_template('admin/dashboard.html', users=users)

@app.route('/admin/create_user/', methods=['GET', 'POST'])
@app.route('/admin/edit_user/<int:user_id>/', methods=['GET', 'POST'])
@login_required
@admin_permission.require()
def create_user(user_id=None):
    """
    Create or edit a user.
    """
    form = ProfileForm()

    if request.method == 'POST':
        if form.validate():
            if user_id != None:
                # Edit a user
                user = User.query.filter(User.id == user_id).first()
                form.populate_obj(user)
                if form.password.data != "":
                    user.set_password(form.password.data)
                db.session.commit()
                flash('User "' + user.firstname + '" successfully updated.', 'success')
            else:
                # Create a new user
                role_user = Role.query.filter(Role.name == "user").first()
                user = User(firstname=form.firstname.data,
                             lastname=form.lastname.data,
                             email=form.email.data,
                             pwdhash=generate_password_hash(form.password.data))
                user.roles.extend([role_user])
                db.session.add(user)
                try:
                    db.session.commit()
                except IntegrityError:
                    flash('Email already used.', 'warning')
                    return redirect(redirect_url())
                flash('User "' + user.firstname + '" successfully created.', 'success')
            return redirect("/admin/edit_user/"+str(user.id)+"/")
        else:
            return render_template('profile.html', form=form)

    if request.method == 'GET':
        if user_id != None:
            user = User.query.filter(User.id == user_id).first()
            form = ProfileForm(obj=user)
            message = "Edit the user <i>" + user.firstname + "</i>"
        else:
            form = ProfileForm()
            message="Add a new user"
        return render_template('/admin/create_user.html', form=form, message=message)

@app.route('/admin/user/<int:user_id>/', methods=['GET'])
@login_required
@admin_permission.require()
def user(user_id=None):
    """
    See information about a user (stations, etc.).
    """
    user = User.query.filter(User.id == user_id).first()
    if user is not None:
        return render_template('/admin/user.html', user=user)
    else:
        flash('This user does not exist.', 'danger')
        return redirect(redirect_url())

@app.route('/admin/delete_user/<int:user_id>/', methods=['GET'])
@login_required
@admin_permission.require()
def delete_user(user_id=None):
    """
    Delete a user (with its stations and measures).
    """
    user = User.query.filter(User.id == user_id).first()
    if user is not None:
        db.session.delete(user)
        db.session.commit()
        flash('User "' + user.firstname + '" successfully deleted.', 'success')
    else:
        flash('This user does not exist.', 'danger')
    return redirect(redirect_url())

@app.route('/admin/enable_user/<int:user_id>/', methods=['GET'])
@app.route('/admin/disable_user/<int:user_id>/', methods=['GET'])
@login_required
@admin_permission.require()
def disable_user(user_id=None):
    """
    Enable or disable the API key of a user.
    """
    user = User.query.filter(User.id == user_id).first()
    if user is not None:
        if user.apikey != "":
            user.apikey = ""
            flash('API key of the user "' + user.firstname + '" successfully disabled.', 'success')
        else:
            import random, base64, hashlib
            user.apikey = base64.b64encode(hashlib.sha512( str(random.getrandbits(256)) ).digest(),
                                                           random.choice(['rA','aZ','gQ','hH','hG','aR','DD'])).rstrip('==')
            flash('API key of the user "' + user.firstname + '" successfully enabled.', 'success')
        db.session.commit()
    else:
        flash('This user does not exist.', 'danger')
    return redirect(redirect_url())
