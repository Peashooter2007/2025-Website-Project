from app import app
from flask import render_template, abort
from flask_sqlalchemy import SQLAlchemy
import os

basedir = os.path.abspath(os.path.dirname(__file__))
db = SQLAlchemy()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
db.init_app(app)

import app.models as models

@app.route('/')
def root():
    return render_template('home.html')

@app.route('/quest/<int:id>')
def quest(id):
    quest = models.Quest.query.filter_by(id=id).first_or_404()
    return render_template('quest.html', quest=quest)   

@app.route('/trader/<int:id>')
def trader(id):
    trader = models.Trader.query.filter_by(id=id).first_or_404()
    return render_template('trader.html', trader=trader)


@app.route('/location/<int:id>')
def location(id):
    location = models.Location.query.filter_by(id=id).first_or_404()
    return render_template('location.html', location=location)


@app.errorhandler(404)
def page_not_found(e):
    return('sum ting wong')



