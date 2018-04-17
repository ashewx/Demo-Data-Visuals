import os
basedir = os.path.abspath(os.path.dirname(__file__))

POSTGRES = {
    'user': 'gkkjrzsf',
    'pw': 'wN_AqVb_CsfndXNEn_j-l-cwZz86VPtU',
    'db': 'gkkjrzsf',
    'host': 'tantor.db.elephantsql.com',
    'port': '5432',
}

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:\
%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'ASUis1stinInnovation'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False