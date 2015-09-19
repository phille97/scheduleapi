# -*- coding: utf-8 -*-

from flask import (
    Blueprint, render_template, abort, flash, session, request,
    redirect, url_for
    )
from flask.ext.login import login_required
from jinja2 import TemplateNotFound


bp = Blueprint('generic', __name__)

@bp.route('/')
def serve_frontpage():
    try:
        return render_template('index.html')
    except TemplateNotFound:
        abort(404)


@bp.route('/about')
def serve_aboutpage():
    try:
        return render_template('about.html')
    except TemplateNotFound:
        abort(404)


@bp.route('/settings', methods=['GET'])
@login_required
def get_settings():
    try:
        return render_template('settings.html')
    except TemplateNotFound:
        abort(404)


@bp.route('/settings', methods=['POST'])
@login_required
def post_settings():
    try:
        return render_template('settings.html')
    except TemplateNotFound:
        abort(404)

