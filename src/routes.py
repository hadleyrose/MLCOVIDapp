from flask import render_template, redirect
from src import app
from src.plotlydash.dashboard import dash_app


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/dash')
def return_dash():
    return render_template('dashboard.html')
