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

from scheduleapi.views.generic import bp as generic_view
from scheduleapi.views.api import bp as api_view


## Load config
config = yaml.load(open('config/config.yml', 'r'))
db_config = config["database"]

## Setup database
from .database.db import db

# Create and setup Flask
app = Flask(__name__)
Bootstrap(app)

## Load and register blueprints
app.register_blueprint(generic_view)
app.register_blueprint(api_view)
