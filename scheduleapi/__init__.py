# -*- coding: utf-8 -*-
#
# Simple schedule API
#
# Author: Philip Johansson <https://github.com/phille97>
#

import os
import time

import yaml

from flask import Flask, Blueprint
from flask_bootstrap import Bootstrap
from flask_restful import Api

from scheduleapi.views.generic import bp as generic_view
from scheduleapi.views.useractions import bp as useraction_view
from scheduleapi.resources.calendar import (
    Calendar, CalendarList, Event, EventList, Occasion, OccasionList
    )


## Load config
config = yaml.load(open('config/config.yml', 'r'))
db_config = config["database"]


## Setup database
from .database.db import db


## Create and setup Flask
app = Flask(__name__)
# Cuz I don't give a fak
Bootstrap(app)


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


## Load and register blueprints
app.register_blueprint(api_bp)
app.register_blueprint(generic_view)
app.register_blueprint(useraction_view)
