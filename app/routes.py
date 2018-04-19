from flask import render_template, flash, redirect, url_for, request, make_response
from app import app, db
import json
from sqlalchemy import create_engine
import decimal, datetime

@app.route('/')
@app.route('/index')
def index():
	return render_template('index.html')
        
        
@app.route('/webhook/<query>', methods=['GET'])
def webhook(query):
	#res = {
	#	"message": query,
	#	"check": 123
	#}
	#res = json.dumps(res, indent=4)

	#r = make_response(res)
	#r.headers['Content-Type'] = 'application/json'
	
	dbengine = create_engine("postgres://gkkjrzsf:wN_AqVb_CsfndXNEn_j-l-cwZz86VPtU@tantor.db.elephantsql.com:5432/gkkjrzsf")
	result = dbengine.execute("SELECT g.name, AVG(r.rating) AS rating FROM genre g, movies m, ratings r, hasagenre h WHERE g.genreid=h.genreid AND m.movieid=h.movieid AND m.movieid=r.movieid GROUP BY g.name ORDER BY g.name;")
	#print (result)
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
