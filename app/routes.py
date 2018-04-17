from flask import render_template, flash, redirect, url_for, request, make_response
from app import app, db
import json

@app.route('/')
@app.route('/index')
def index():
	return render_template('index.html')
        
        
@app.route('/webhook/<query>', methods=['GET'])
def webhook(query):
	res = {
		"message": query,
		"check": 123
	}
	res = json.dumps(res, indent=4)

	r = make_response(res)
	r.headers['Content-Type'] = 'application/json'
	return r