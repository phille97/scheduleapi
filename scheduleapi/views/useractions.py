# -*- coding: utf-8 -*-

from flask import (
    Blueprint, render_template, abort, flash, session, request,
    redirect, url_for
    )
from jinja2 import TemplateNotFound

from ..forms.useractions import Login as LoginForm, Register as RegisterForm


bp = Blueprint('useractions', __name__, url_prefix='/usr')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and  form.validate():
        # Do login
        return redirect(url_for('generic.serve_frontpage'))
    try:
        return render_template('forms/login.html', form=form)
    except TemplateNotFound:
        abort(404)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and  form.validate():
        # Do register
        flash('Registered successfully. You may now login')
        return redirect(url_for('useractions.login'))
    try:
        return render_template('forms/register.html', form=form)
    except TemplateNotFound:
        abort(404)

@bp.route('/logout', methods=['GET'])
def do_logout():
    abort(501)