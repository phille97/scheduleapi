# -*- coding: utf-8 -*-

from flask import (
    Blueprint, render_template, abort, flash, session, request,
    redirect, url_for
    )
from jinja2 import TemplateNotFound


bp = Blueprint('generic', __name__)

@bp.route('/')
def serve_frontpage():
    try:
        return render_template('index.html')
    except TemplateNotFound:
        abort(404)