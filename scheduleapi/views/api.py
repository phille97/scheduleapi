# -*- coding: utf-8 -*-

from flask import (
    Blueprint, render_template, abort, flash, session, request,
    redirect, url_for
    )
from jinja2 import TemplateNotFound


bp = Blueprint('api', __name__, url_prefix='/api')
