from __future__ import print_function
import sys
import json
#from future.standard_library import install_aliases
#install_aliases()

# from urllib.parse import urlparse, urlencode
# from urllib.request import urlopen, Request
# from urllib.error import HTTPError

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from configuration import Config

app = Flask(__name__)

app.config['DEBUG'] = True

#Configuration of application is located in configuration.py
app.config.from_object(Config)

bs = Bootstrap(app) #flask-bootstrap
db = SQLAlchemy(app) #flask-sqlalchemy
migrate = Migrate(app, db)

from app import routes, models