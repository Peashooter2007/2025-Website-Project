from app import app
from flask import render_template, abort, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

basedir = os.path.abspath(os.path.dirname(__file__))
db = SQLAlchemy()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
db.init_app(app)
app.secret_key = 'correcthorsebatterystaple'
WTF_CSRF_ENABLED = True
WTF_CSRF_SECRET_KEY = 'sup3r_secr3t_passw3rd'

import app.models as models
from app.forms import Add_Quest

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

@app.route('/add_quest', methods=['GET', 'POST'])
def add_quest():
    form = Add_Quest()
    traders = models.Trader.query.all()
    form.trader.choices =[(trader.id, trader.name) for trader in traders]
    if request.method=='POST' and form.validate_on_submit():
        new_quest = models.Quest()
        new_quest.name = form.name.data
        new_quest.desc = form.desc.data
        new_quest.lvl = form.lvl.data
        new_quest.exp = form.exp.data
        new_quest.trader = form.trader.data
        db.session.add(new_quest)
        db.session.commit()
        return redirect(url_for('quest', id=new_quest.id))        
    else:
        return render_template('add_quest.html', form=form, page_title="Add a Quest")

@app.errorhandler(404)
def page_not_found(e):
    return('No Such Webpage!')
