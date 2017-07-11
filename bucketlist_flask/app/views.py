# views.py

from flask import render_template, Flask, redirect, request

from app import app

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/add' methods=['GET', 'POST'])
def create_bucketlist():
	if request.method == 'POST':
		
	