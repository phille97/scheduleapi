# -*- coding: utf-8 -*-

from flask import (
    Blueprint, render_template, abort, flash, session, request,
    redirect, url_for
    )
from jinja2 import TemplateNotFound


bp = Blueprint('useractions', __name__, url_prefix='/usr')

@bp.route('/login', methods=['GET'])
def get_login():
    try:
        return render_template('forms/login.html')
    except TemplateNotFound:
        abort(404)

@bp.route('/register', methods=['GET'])
def get_register():
    try:
        return render_template('forms/register.html')
    except TemplateNotFound:
        abort(404)


@bp.route('/login', methods=['POST'])
def do_login():
    abort(501)

@bp.route('/register', methods=['POST'])
def do_register():
    abort(501)

@bp.route('/logout', methods=['GET'])
def do_logout():
    abort(501)