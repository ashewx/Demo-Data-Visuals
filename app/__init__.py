from __future__ import print_function
#from future.standard_library import install_aliases
#install_aliases()

# from urllib.parse import urlparse, urlencode
# from urllib.request import urlopen, Request
# from urllib.error import HTTPError

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from configuration import Config

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:\
%(pw)s@%(host)s:%(port)s/%(db)s' % configuration.POSTGRES

app.config['DEBUG'] = True

#Configuration of application, see configuration.py, choose one and uncomment.
#app.config.from_object('configuration.ProductionConfig')
#app.config.from_object('configuration.TestingConfig')
app.config.from_object(Config)

bs = Bootstrap(app) #flask-bootstrap
db = SQLAlchemy(app) #flask-sqlalchemy

from app import routes, models