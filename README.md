# Demo Data Visuals
Movie Recommendation Database  
Build a web application

Our web application must be run in Python 2.7 (Don't even attempt using Python 3)

## Installation
Install all dependencies necessary to run:

    $ pip install -r requirements.txt

Change the FLASK_APP environment variable:

	$ export FLASK_APP=run.py
If you are using Microsoft Windows, use `set` instead of `export` in the command above.

Then, run the application with python:

	$ python run.py

To see your application, access this url in your browser: 

	http://localhost:5000

All configuration settings are located in: `app/configuration.py`

The site is also currently deployed and hosted on Heroku and is using an ElephantSQL Cloud Postgres database to hold all movie data (this only allows 5 simultaneous connections to the database):

	https://cse412-web.herokuapp.com/
