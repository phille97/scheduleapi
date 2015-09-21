# -*- coding: utf-8 -*-
#
# Simple schedule API
#
# Author: Philip Johansson <https://github.com/phille97>
#

import os
import time

import yaml

from flask import Flask, Blueprint, g
from flask_bootstrap import Bootstrap
from flask_restful import Api
from flask_login import LoginManager

from scheduleapi.views.generic import bp as generic_view
from scheduleapi.views.useractions import bp as useraction_view
from scheduleapi.resources.calendar import (
    Calendar, CalendarList, Event, EventList, Occasion, OccasionList
    )


## Load config
config = yaml.load(open('config/config.yml', 'r'))
db_config = config["database"]
flask_config = config["flask"]

## Setup database
from .database.db import DATABASE_URI, session
from .database.models import User

## Create and setup Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = flask_config['secret_key']
app.config['DATABASE_URI'] = DATABASE_URI
app.session = session

## LoginManager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_message = u"Please authenticate!"
login_manager.login_view = "useractions.login"

@login_manager.user_loader
def user_loader(user_id):
    return session.query(User).filter(User.id==user_id).first()

## API Blueprint
api_bp = Blueprint('api', __name__, url_prefix='/api')

## API v1
api_v1 = Api(api_bp, default_mediatype='application/json', prefix='/v1')

api_v1.add_resource(CalendarList, '/calendars')
api_v1.add_resource(Calendar, '/calendars/<calendar_id>')

api_v1.add_resource(EventList, '/calendars/<calendar_id>/events')
api_v1.add_resource(Event, '/events/<event_id>')

api_v1.add_resource(OccasionList, '/events/<event_id>/occasions')
api_v1.add_resource(Occasion, '/events/<event_id>/occasions/<occasion_id>')


# Cuz I don't give a fak
Bootstrap(app)

## Load and register blueprints
app.register_blueprint(api_bp)
app.register_blueprint(generic_view)
app.register_blueprint(useraction_view)
