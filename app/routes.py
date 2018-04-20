from flask import render_template, flash, redirect, url_for, request, make_response
from app import app, db
import json
from sqlalchemy import create_engine
import decimal, datetime

# Connect to SQL Movie database
dbengine = create_engine("postgres://gkkjrzsf:wN_AqVb_CsfndXNEn_j-l-cwZz86VPtU@tantor.db.elephantsql.com:5432/gkkjrzsf")

@app.route('/')
@app.route('/index')
def index():
	return render_template('index.html')        
        
@app.route('/average', methods=['GET'])
def average():	
	# Retrieve URL parameters
	min = request.args.get('min', None)  # use default value replace 'None'
	max = request.args.get('max', None)
	title_keyword = request.args.get('title', None)
	tag_keyword = request.args.get('tag', None)
	
	# Generate the SQL query for given parameters
	if min == None and max == None and title_keyword == None and tag_keyword == None:
		sql_query = "SELECT g.name, AVG(r.rating) AS rating FROM genre g, movies m, ratings r, hasagenre h WHERE g.genreid=h.genreid AND m.movieid=h.movieid AND m.movieid=r.movieid GROUP BY g.name ORDER BY g.name;"
	elif min != None and max != None:
		sql_query = "SELECT g.name, AVG(r.rating) AS rating FROM genre g, movies m, ratings r, hasagenre h WHERE g.genreid=h.genreid AND m.movieid=h.movieid AND m.movieid=r.movieid AND r.rating >= {0} AND r.rating <= {1} GROUP BY g.name ORDER BY g.name;".format(min, max)
	else:
		sql_query = ""
	result = dbengine.execute(sql_query)
	#print (result)
	r = (json.dumps([dict(r) for r in result], default=alchemyencoder))
	r = make_response(r)
	r.headers['Content-Type'] = 'application/json'
	return r
	
@app.route('/count', methods=['GET']) # Example /count?min=<min>&max=<max>&title=<title_keyword>&tag=<tag_keyword>
def count():	
	# Retrieve URL parameters
	min = request.args.get('min', None)  # use default value replace 'None'
	max = request.args.get('max', None)
	title_keyword = request.args.get('title', None)
	tag_keyword = request.args.get('tag', None)
	
	# Generate the SQL query for given parameters
	if min == None and max == None and title_keyword == None and tag_keyword == None:
		sql_query = "SELECT g.name, COUNT(*) AS moviecount FROM genre g, movies m, hasagenre h WHERE g.genreid=h.genreid AND m.movieid=h.movieid GROUP BY g.name ORDER BY g.name;"
	elif min != None and max != None:
		sql_query = "SELECT g.name, COUNT(m.movieid) AS moviecount FROM genre g, movies m, ratings r, hasagenre h WHERE g.genreid=h.genreid AND m.movieid=h.movieid AND m.movieid=r.movieid AND r.rating >= {0} AND r.rating <= {1} GROUP BY g.name ORDER BY g.name;".format(min, max)
		print sql_query
	else:
		sql_query = ""
	result = dbengine.execute(sql_query)
	r = (json.dumps([dict(r) for r in result], default=alchemyencoder))
	r = make_response(r)
	r.headers['Content-Type'] = 'application/json'
	return r
	
def alchemyencoder(obj):
    """JSON encoder function for SQLAlchemy special classes."""
    if isinstance(obj, datetime.date):
        return obj.isoformat()
    elif isinstance(obj, decimal.Decimal):
        return float(obj)
