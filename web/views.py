#! /usr/bin/env python
# -*- coding: utf-8 -*-

from flask import render_template, jsonify, request, flash, session, url_for, redirect, g
from flask.ext.login import LoginManager, login_user, logout_user, login_required, current_user, AnonymousUserMixin

from web import app, db
from web.models import User, Station
from forms import SigninForm, ProfileForm, StationForm


login_manager = LoginManager()
login_manager.init_app(app)

@app.before_request
def before_request():
    g.user = current_user
    if g.user.is_authenticated():
        pass
        #g.user.last_seen = datetime.utcnow()
        #db.session.add(g.user)
        #db.session.commit()

@app.errorhandler(403)
def authentication_failed(e):
    flash('Authentication failed.', 'danger')
    return redirect(url_for('login'))

@app.errorhandler(401)
def authentication_failed(e):
    flash('Authentication required.', 'info')
    return redirect(url_for('login'))

@login_manager.user_loader
def load_user(email):
    # Return an instance of the User model
    return User.query.filter(User.email == email).first()

@app.route('/login/', methods=['GET', 'POST'])
def login():
    g.user = AnonymousUserMixin()
    form = SigninForm()

    if form.validate_on_submit():
        user = User.query.filter(User.email == form.email.data).first()
        login_user(user)
        g.user = user
        flash("Logged in successfully.", 'success')
        return redirect(url_for('profile'))
    return render_template('login.html', form=form)

@app.route('/logout/')
@login_required
def logout():
    """
    Remove the user information from the session.
    """
    logout_user()
    flash("Logged out successfully.", 'success')
    return redirect(url_for('map_view'))

def redirect_url(default='map_view'):
    return request.args.get('next') or \
            request.referrer or \
            url_for(default)




@app.route('/', methods=['GET'])
@app.route('/map/', methods=['GET'])
def map_view():
    """
    Main view which displays all public stations.
    """
    return render_template('map.html')

@app.route('/profile/', methods=['GET', 'POST'])
@login_required
def profile():
    """
    Edit the profile of the user.
    """
    user = User.query.filter(User.email == g.user.email).first()
    form = ProfileForm()
    forms_station = []
    for _ in user.stations:
        forms_station.append(StationForm())

    if request.method == 'POST':
        if form.validate():
            form_station = StationForm(obj=user.stations[0])
            form.populate_obj(user)
            if form.password.data != "":
                user.set_password(form.password.data)
            db.session.commit()
            flash('User "' + user.firstname + '" successfully updated', 'success')

        for form_station in forms_station:
            if form_station.validate():
                form = ProfileForm(obj=user)
                for station in user.stations:
                    if station.name == form_station.name.data:
                        form_station.populate_obj(station)
                        db.session.commit()
                        flash('Station "' + station.name + '" successfully updated', 'success')
                    break

        if not (form.validate() or any([form_station.validate() for form_station in forms_station])):
            return render_template('profile.html', form=form, forms_station=forms_station)

        return redirect(url_for('profile'))

    if request.method == 'GET':
        form = ProfileForm(obj=user)
        forms_station = []
        for form_station in user.stations:
            forms_station.append(StationForm(obj=form_station))
        return render_template('profile.html', form=form, forms_station=forms_station)