# -*- coding: utf-8 -*-
#
# Simple schedule API
#
# Author: Philip Johansson <https://github.com/phille97>
#

import os
import time

import yaml
from flask import Flask, jsonify, send_from_directory, request
from flask_bootstrap import Bootstrap
from flask_restful import Api

from scheduleapi.views.generic import bp as generic_view
from scheduleapi.views.useractions import bp as useraction_view


## Load config
config = yaml.load(open('config/config.yml', 'r'))
db_config = config["database"]

## Setup database
from .database.db import db

# Create and setup Flask
app = Flask(__name__)
app.config['BUNDLE_ERRORS'] = True

# Cuz i don't give a fak
Bootstrap(app)

# API v1
api_v1 = Api(app, catch_all_404s=True)
from scheduleapi.views.api import api as api_v1

## Load and register blueprints
app.register_blueprint(generic_view)
app.register_blueprint(useraction_view)
