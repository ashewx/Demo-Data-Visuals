import json
import decimal, datetime
from flask import render_template, flash, redirect, url_for, request, make_response
from sqlalchemy import create_engine
from app import app, db


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
	if min == None and max == None and title_keyword == None and tag_keyword == None: # /average
		sql_query = "SELECT g.name, AVG(r.rating) AS rating" \
					" FROM genre g, movies m, ratings r, hasagenre h " \
					" WHERE g.genreid=h.genreid AND m.movieid=h.movieid AND m.movieid=r.movieid" \
					" GROUP BY g.name" \
					" ORDER BY g.name;"
	else:
		if min != None and max != None:
			if title_keyword != None:
				if tag_keyword != None: # /average?min=<min>&max=<max>&title=<title_keyword>&tag=<tag_keyword>
					sql_query = "SELECT g.name, AVG(r.rating) AS rating" \
								" FROM genre g, movies m, ratings r, hasagenre h, tags t, taginfo ti" \
								" WHERE g.genreid=h.genreid AND m.movieid=h.movieid AND m.movieid=r.movieid AND m.movieid=t.movieid AND t.tagid=ti.tagid AND r.rating >= {0} AND r.rating <= {1} OR r.rating = 0 AND LOWER(m.title) LIKE LOWER('%%{2}%%') AND LOWER(ti.content) LIKE LOWER('%%{3}%%')" \
								" GROUP BY g.name" \
								" ORDER BY g.name;".format(min, max, title_keyword, tag_keyword)
				else: # /average?min=<min>&max=<max>&title=<title_keyword>
					sql_query = "SELECT g.name, AVG(r.rating) AS rating" \
								" FROM genre g, movies m, ratings r, hasagenre h" \
								" WHERE g.genreid=h.genreid AND m.movieid=h.movieid AND m.movieid=r.movieid AND r.rating >= {0} AND r.rating <= {1} AND LOWER(m.title) LIKE LOWER('%%{2}%%')" \
								" GROUP BY g.name" \
								" ORDER BY g.name;".format(min, max, title_keyword)
			elif tag_keyword != None: #/average?min=<min>&max=<max>&tag=<tag_keyword>
				sql_query = "SELECT g.name, AVG(r.rating) AS rating" \
							" FROM genre g, movies m, ratings r, hasagenre h, tags t, taginfo ti" \
							" WHERE g.genreid=h.genreid AND m.movieid=h.movieid AND m.movieid=r.movieid AND m.movieid=t.movieid AND t.tagid=ti.tagid AND r.rating >= {0} AND r.rating <= {1} AND LOWER(ti.content) LIKE LOWER('%%{2}%%')" \
							" GROUP BY g.name" \
							" ORDER BY g.name;".format(min, max, tag_keyword)
			else: # /average?min=<min>&max=<max>
				sql_query = "SELECT g.name, AVG(r.rating) AS rating" \
							" FROM genre g, movies m, ratings r, hasagenre h" \
							" WHERE g.genreid=h.genreid AND m.movieid=h.movieid AND m.movieid=r.movieid AND r.rating >= {0} AND r.rating <= {1}" \
							" GROUP BY g.name" \
							" ORDER BY g.name;".format(min, max)
	
	# Retrieve Json string and format to Json object
	result = dbengine.execute(sql_query)
	r = (json.dumps([dict(r) for r in result], default=alchemyencoder))
	r = make_response(r)
	r.headers['Content-Type'] = 'application/json'
	return r
	
@app.route('/count', methods=['GET'])
def count():	
	# Retrieve URL parameters
	min = request.args.get('min', None)  # use default value replace 'None'
	max = request.args.get('max', None)
	title_keyword = request.args.get('title', None)
	tag_keyword = request.args.get('tag', None)
	null_keyword = request.args.get('null', None)
	if null_keyword == "true":
		null_keyword = True
	else:
		null_keyword = False
	
	# Generate the SQL query for given parameters
	if min == None and max == None and title_keyword == None and tag_keyword == None: # /count
		sql_query = "SELECT g.name, COUNT(*) AS moviecount" \
					" FROM genre g, movies m, hasagenre h, ratings r" \
					" WHERE g.genreid=h.genreid AND m.movieid=h.movieid AND m.movieid=r.movieid" \
					" GROUP BY g.name" \
					" ORDER BY g.name;"
	else:
		if min != None and max != None:
			if title_keyword != None: 
				if tag_keyword != None: 
					if null_keyword: # /count?min=<min>&max=<max>&title=<title_keyword>&tag=<tag_keyword>&null=<null_keyword>
						sql_query = "SELECT g.name, COUNT(m.movieid) AS moviecount" \
									" FROM genre g, movies m, hasagenre h, tags t, taginfo ti" \
									" WHERE g.genreid=h.genreid AND m.movieid=h.movieid AND m.movieid=t.movieid AND t.tagid=ti.tagid AND LOWER(m.title) LIKE LOWER('%%{2}%%') AND LOWER(ti.content) LIKE LOWER('%%{3}%%') AND (m.movieid IN (SELECT r.movieid FROM ratings r WHERE r.rating >= {0} AND r.rating <= {1}) OR m.movieid NOT IN (SELECT r1.movieid FROM ratings r1))" \
									" GROUP BY g.name" \
									" ORDER BY g.name;".format(min, max, title_keyword, tag_keyword)
					else: # /count?min=<min>&max=<max>&title=<title_keyword>&tag=<tag_keyword>
						sql_query = "SELECT g.name, COUNT(m.movieid) AS moviecount" \
									" FROM genre g, movies m, ratings r, hasagenre h, tags t, taginfo ti" \
									" WHERE g.genreid=h.genreid AND m.movieid=h.movieid AND m.movieid=r.movieid AND m.movieid=t.movieid AND t.tagid=ti.tagid AND r.rating >= {0} AND r.rating <= {1} AND LOWER(m.title) LIKE LOWER('%%{2}%%') AND LOWER(ti.content) LIKE LOWER('%%{3}%%')" \
									" GROUP BY g.name" \
									" ORDER BY g.name;".format(min, max, title_keyword, tag_keyword)
				else: 
					if null_keyword: # /count?min=<min>&max=<max>&title=<title_keyword>&null=<null_keyword>
						sql_query = "SELECT g.name, COUNT(m.movieid) AS moviecount" \
									" FROM genre g, movies m, hasagenre h" \
									" WHERE g.genreid=h.genreid AND m.movieid=h.movieid AND LOWER(m.title) LIKE LOWER('%%{2}%%') AND (m.movieid IN (SELECT r.movieid FROM ratings r WHERE r.rating >= {0} AND r.rating <= {1}) OR m.movieid NOT IN (SELECT r1.movieid FROM ratings r1))" \
									" GROUP BY g.name" \
									" ORDER BY g.name;".format(min, max, title_keyword)
					else: # /count?min=<min>&max=<max>&title=<title_keyword>
						sql_query = "SELECT g.name, COUNT(m.movieid) AS moviecount" \
									" FROM genre g, movies m, ratings r, hasagenre h" \
									" WHERE g.genreid=h.genreid AND m.movieid=h.movieid AND m.movieid=r.movieid AND r.rating >= {0} AND r.rating <= {1} AND LOWER(m.title) LIKE LOWER('%%{2}%%')" \
									" GROUP BY g.name" \
									" ORDER BY g.name;".format(min, max, title_keyword)
			elif tag_keyword != None:
				if null_keyword: # /count?min=<min>&max=<max>&tag=<tag_keyword>&null=<null_keyword>
					sql_query = "SELECT g.name, COUNT(DISTINCT m.movieid) AS moviecount" \
								" FROM genre g, movies m, hasagenre h, tags t, taginfo ti" \
								" WHERE g.genreid=h.genreid AND m.movieid=h.movieid AND m.movieid=t.movieid AND t.tagid=ti.tagid AND LOWER(ti.content) LIKE LOWER('%%{2}%%') AND (m.movieid IN (SELECT r.movieid FROM ratings r WHERE r.rating >= {0} AND r.rating <= {1}) OR m.movieid NOT IN (SELECT r1.movieid FROM ratings r1))" \
								" GROUP BY g.name" \
								" ORDER BY g.name;".format(min, max, tag_keyword)
				else:  # /count?min=<min>&max=<max>&tag=<tag_keyword>
					sql_query = "SELECT g.name, COUNT(m.movieid) AS moviecount" \
								" FROM genre g, movies m, ratings r, hasagenre h, tags t, taginfo ti" \
								" WHERE g.genreid=h.genreid AND m.movieid=h.movieid AND m.movieid=r.movieid AND m.movieid=t.movieid AND t.tagid=ti.tagid AND r.rating >= {0} AND r.rating <= {1} AND LOWER(ti.content) LIKE LOWER('%%{2}%%')" \
								" GROUP BY g.name" \
								" ORDER BY g.name;".format(min, max, tag_keyword)
			else: 
				if null_keyword: # /count?min=<min>&max=<max>&null=<null_keyword>
					sql_query = "SELECT g.name, COUNT(m.movieid) AS moviecount" \
								" FROM genre g, movies m, hasagenre h" \
								" WHERE g.genreid=h.genreid AND m.movieid=h.movieid AND (m.movieid IN (SELECT r.movieid FROM ratings r WHERE r.rating >= {0} AND r.rating <= {1}) OR m.movieid NOT IN (SELECT r1.movieid FROM ratings r1))" \
								" GROUP BY g.name" \
								" ORDER BY g.name;".format(min, max)
				else: # /count?min=<min>&max=<max>
					sql_query = "SELECT g.name, COUNT(m.movieid) AS moviecount" \
								" FROM genre g, movies m, ratings r, hasagenre h" \
								" WHERE g.genreid=h.genreid AND m.movieid=h.movieid AND m.movieid=r.movieid AND r.rating >= {0} AND r.rating <= {1}" \
								" GROUP BY g.name" \
								" ORDER BY g.name;".format(min, max)

	# Retrieve Json string and format to Json object
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
       