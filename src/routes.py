from flask import render_template, redirect
from src import app
from src.plotlydash.dashboard2 import dash_app2


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/dash')
def return_dash():
    return render_template('dashboard.html')
