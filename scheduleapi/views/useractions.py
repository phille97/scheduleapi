# -*- coding: utf-8 -*-

from flask import (
    Blueprint, render_template, abort, flash, session, request,
    redirect, url_for
    )
from flask.ext.login import login_user
from jinja2 import TemplateNotFound

from ..forms.useractions import Login as LoginForm, Register as RegisterForm
from ..controllers.users import (
    login as do_login, register as do_register, logout as do_logout
    )
from ..database.models import User


bp = Blueprint('useractions', __name__, url_prefix='/usr')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        if login_user(User(form.data['username'], form.data['password'])):
            flash("You are now logged in!")
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
    abort(501)