from app import app
from flask import render_template, abort, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os
from werkzeug.utils import secure_filename

basedir = os.path.abspath(os.path.dirname(__file__))
db = SQLAlchemy()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
db.init_app(app)
app.secret_key = 'correcthorsebatterystaple'

import app.models as models
from app.forms import Add_Quest, Add_Trader, Add_Location, Searchbar

@app.route('/')
def root():
    return render_template('home.html', page_title = 'Home')

@app.route('/quests', methods = ['GET', 'POST'])
def quests():
    quests = models.Quest.query.all()
    form = Searchbar()
    if form.validate_on_submit():
        search_query = form.search.data
        quests = models.Quest.query.filter(models.Quest.name.ilike(f'%{search_query}%')).all()
    return render_template('quests.html', quests=quests, page_title = 'Quests', form=form)

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
    return render_template('edit.html', page_title = "Edit")

@app.route('/add_quest', methods=['GET', 'POST'])
def add_quest():
    form = Add_Quest()
    quest_images = 'app/static/images/quests/'
    traders = models.Trader.query.all()
    form.trader.choices =[(trader.id, trader.name) for trader in traders]
    formpassword = models.Password.query.first()
    password = formpassword.password
    if request.method=='POST' and form.validate_on_submit() and form.password.data == password:
        image = request.files['image']
        imagename = secure_filename(form.image.data.filename)
        image.save(quest_images+imagename)
        new_quest = models.Quest()
        new_quest.name = form.name.data
        new_quest.desc = form.desc.data
        new_quest.lvl = form.lvl.data
        new_quest.exp = form.exp.data
        new_quest.trader = form.trader.data
        new_quest.image = imagename
        db.session.add(new_quest)
        db.session.commit()
        return redirect(url_for('quest', id=new_quest.id))     
    else:
        return render_template('add_quest.html', form=form, page_title="Add a Quest")

@app.route('/add_trader', methods=['GET', 'POST'])
def add_trader():
    form = Add_Trader()
    trader_images = 'app/static/images/traders/'
    if request.method=='POST' and form.validate_on_submit():
        image = request.files['image']
        imagename = secure_filename(form.image.data.filename)
        image.save(trader_images+imagename)
        new_trader = models.Trader()
        new_trader.name = form.name.data
        new_trader.desc = form.desc.data
        new_trader.image = imagename
        db.session.add(new_trader)
        db.session.commit()
        return redirect(url_for('trader', id=new_trader.id))  
    else:
        return render_template('add_trader.html', form=form, page_title ="Add a Trader")
    
@app.route('/add_location', methods=['GET', 'POST'])
def add_location():
    form = Add_Location()
    location_images = 'app/static/images/locations/'
    if request.method=='POST' and form.validate_on_submit():
        image = request.files['image']
        imagename = secure_filename(form.image.data.filename)
        image.save(location_images+imagename)
        map = request.files['map']
        mapname = secure_filename(form.map.data.filename)
        map.save(location_images+mapname)
        new_location = models.Location()
        new_location.name = form.name.data
        new_location.desc = form.desc.data
        new_location.image = imagename
        new_location.map = mapname
        db.session.add(new_location)
        db.session.commit()
        return redirect(url_for('location', id=new_location.id))  
    else:
        return render_template('add_location.html', form=form, page_title ="Add a Location")

@app.errorhandler(404)
def page_not_found(e):
    return('No Such Webpage!')
