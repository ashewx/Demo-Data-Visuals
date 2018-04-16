from flask import render_template, flash, redirect, url_for, request
from app import app, db

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')
        
        
@app.route('/webhook', methods=['POST'])
def webhook():
    return null