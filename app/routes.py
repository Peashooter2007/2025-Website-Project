from app import app
from flask import render_template, abort, request
from flask_sqlalchemy import SQLAlchemy
import os

basedir = os.path.abspath(os.path.dirname(__file__))
db = SQLAlchemy()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
db.init_app(app)

import app.models as models

@app.route('/')
def root():
    return render_template('home.html', page_title = 'Home')

@app.route('/quests')
def quests():
    quests = models.Quest.query.all()
    return render_template('quests.html', quests=quests, page_title = 'Quests')

@app.route('/traders')
def traders():
    traders = models.Trader.query.all()
    return render_template('traders.html', traders=traders, page_title = 'Traders')

@app.route('/locations')
def locations():
    locations = models.Location.query.all()
    return render_template('locations.html', locations=locations, page_title = 'Locations')

@app.route('/quest/<int:id>')
def quest(id):
    quest = models.Quest.query.filter_by(id=id).first_or_404()
    return render_template('quest.html', quest=quest, page_title = quest)   

@app.route('/trader/<int:id>')
def trader(id):
    trader = models.Trader.query.filter_by(id=id).first_or_404()
    return render_template('trader.html', trader=trader, page_title = trader)


@app.route('/location/<int:id>')
def location(id):
    location = models.Location.query.filter_by(id=id).first_or_404()
    return render_template('location.html', location=location, page_title = location)

@app.route('/edit')
def edit():
    return render_template('edit.html', page_title = 'Edit')

@app.route('/add', methods = ['GET','POST'])
def add():
    print(request.args.get('quest'))
    return 'Done'



@app.errorhandler(404)
def page_not_found(e):
    return('No Such Webpage!')
