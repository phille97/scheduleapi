# -*- coding: utf-8 -*-
#
# Simple schedule API
#
# Author: Philip Johansson <https://github.com/phille97>
#

import os
import time

import yaml
import wtforms_json

from flask import Flask, Blueprint, g, jsonify
from flask_bootstrap import Bootstrap
from flask_restful import Api
from flask_login import LoginManager
from flask_debugtoolbar import DebugToolbarExtension

from scheduleapi.views.generic import bp as generic_view
from scheduleapi.views.useractions import bp as useraction_view
from scheduleapi.resources.calendar import api as api_v1


# Load config
config = yaml.load(open('config/config.yml', 'r'))
db_config = config["database"]
flask_config = config["flask"]

# Setup database
from .database.db import DATABASE_URI, session, engine
from .database.models import User, Apikey

# Create and setup Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = flask_config['secret_key']
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
app.session = session

## To be used only in development
from flask.ext.sqlalchemy import _EngineDebuggingSignalEvents
from flask_debugtoolbar import DebugToolbarExtension
#app.config['DEBUG_TB_ENABLED'] = True
#app.config['DEBUG_TB_PROFILER_ENABLED'] = True
#app.config['DEBUG_TB_TEMPLATE_EDITOR_ENABLED'] = True
#toolbar = DebugToolbarExtension(app)
#_EngineDebuggingSignalEvents(engine, app.import_name).register()

# Bootstrap... Cuz I don't give a fak
Bootstrap(app)
app.config['BOOTSTRAP_SERVE_LOCAL'] = True

# WTForms
wtforms_json.init()

# LoginManager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_message = u"Please authenticate!"
login_manager.login_view = "useractions.login"


@login_manager.user_loader
def user_loader(user_id):
    return session.query(User).filter(User.id == user_id).first()


@login_manager.request_loader
def load_user_from_request(request):
    api_key = request.headers.get('apikey')
    api_pass = request.headers.get('apipass')

    if api_key and api_pass:
        return session.query(User).filter(Apikey.keyid == api_key)\
                                  .filter(Apikey.keypass == api_pass).first()

    return None


# API schtuff
api_bp = Blueprint('api', __name__, url_prefix='/api/v1')
api_v1.init_app(api_bp)


@api_bp.errorhandler(404)
def route_not_found(e):
    return jsonify('Fuck you')


# Load and register blueprints
app.register_blueprint(api_bp)
app.register_blueprint(generic_view)
app.register_blueprint(useraction_view)
