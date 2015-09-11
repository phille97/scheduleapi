#
# Simple schedule API
#
# Author: Philip Johansson <https://github.com/phille97>
#

import time

from flask import Flask, jsonify, send_from_directory, request

# Create the application
app = Flask(__name__)

@app.route('/')
def render_webpage():
    return 'Hello World'
