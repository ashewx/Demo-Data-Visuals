from __future__ import print_function
#from future.standard_library import install_aliases
#install_aliases()

from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError

import json
import os

from flask import Flask, request, make_response, render_template
from pip._vendor.requests.sessions import session

# Flask app should start in global layout
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/webhook', methods=['POST'])
def webhook():
    return null

