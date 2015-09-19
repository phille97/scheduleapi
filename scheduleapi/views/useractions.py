# -*- coding: utf-8 -*-

import flask
from flask import (
    Blueprint, render_template, abort, flash, session, request,
    redirect, url_for
    )
from flask.ext.login import login_user, logout_user
from jinja2 import TemplateNotFound

from ..forms.useractions import Login as LoginForm, Register as RegisterForm
from ..controllers.users import register as do_register, encrypt_password, check_password
from ..controllers.database import get_session
from ..database.models import User


bp = Blueprint('useractions', __name__, url_prefix='/usr')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        session = get_session()
        user = session.query(User).filter(User.username==form.username.data).first()
        if user:
            if check_password(form.password.data, user.password):
                user.authenticated = True
                session.add(user)
                session.commit()
                login_user(user, remember=form.remember_me.data)
                return redirect(url_for('generic.serve_frontpage'))
        else:
            flash("Invalid credentials!")
    try:
        return render_template('forms/login.html', form=form)
    except TemplateNotFound:
        abort(404)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and  form.validate():
        if do_register(form.data['username'], form.data['password'], form.data['email']):
            flash("Registered successfully. You may now login")
            return redirect(url_for('useractions.login'))
        else:
            flash("Username already taken!")
    try:
        return render_template('forms/register.html', form=form)
    except TemplateNotFound:
        abort(404)

@bp.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return redirect(url_for('generic.serve_frontpage'))