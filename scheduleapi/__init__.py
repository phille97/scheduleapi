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

## Load config
config = yaml.load(open('config/config.yml', 'r'))
db_config = config["database"]

## Setup database
from .database.db import db

# Create the application
app = Flask(__name__)

## Load and register blueprints
