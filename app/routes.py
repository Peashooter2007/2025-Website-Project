from app import app
from flask import render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
import os
from werkzeug.utils import secure_filename

basedir = os.path.abspath(os.path.dirname(__file__))
db = SQLAlchemy()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
db.init_app(app)
app.secret_key = 'correcthorsebatterystaple'

import app.models as models  # NOQA
from app.forms import (Add_Quest, Add_Trader, Add_Location, Searchbar, Add_Reward, Add_Objective,
                       Delete_Quest, Delete_Trader, Delete_Location,
                       Connect_Location, Connect_Quests,
                       Login
                       )

ALLOWED_EXTENSIONS = set(['pdf', 'png', 'jpg', 'jpeg'])

USERNAME = "admin"
PASSWORD = "password123"


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# home page
@app.route('/')
def root():
    return render_template('home.html', page_title='Home')


# list of all quests
@app.route('/quests', methods=['GET', 'POST'])
def quests():
    quests = models.Quest.query.all()
    form = Searchbar()
    if form.validate_on_submit():
        search_query = form.search.data
        quests = models.Quest.query.filter(models.Quest.name.ilike(f'%{search_query}%')).all()
    return render_template('quests.html', quests=quests, page_title='Quests', form=form)


# list of all traders
@app.route('/traders')
def traders():
    traders = models.Trader.query.all()
    return render_template('traders.html', traders=traders, page_title='Traders')


# list of all locations
@app.route('/locations')
def locations():
    locations = models.Location.query.all()
    return render_template('locations.html', locations=locations, page_title='Locations')


# information page for quest with id
@app.route('/quest/<int:id>')
def quest(id):
    quest = models.Quest.query.filter_by(id=id).first_or_404()
    return render_template('quest.html', quest=quest, page_title=quest)


# information page for trader with id
@app.route('/trader/<int:id>')
def trader(id):
    trader = models.Trader.query.filter_by(id=id).first_or_404()
    return render_template('trader.html', trader=trader, page_title=trader)


# information page for location with id
@app.route('/location/<int:id>')
def location(id):
    location = models.Location.query.filter_by(id=id).first_or_404()
    return render_template('location.html', location=location, page_title=location)


# admin login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = Login()
    if request.method == 'POST' and form.validate_on_submit:
        username = form.username.data
        password = form.password.data
        if username == USERNAME and password == PASSWORD:
            session['username'] = username
            return redirect("/")
        else:
            login_error = "Username or password was incorrect. Please try again."
            return render_template('login.html', form=form, login_error=login_error, page_title="Admin Login")
    else:
        return render_template('login.html', form=form, page_title="Admin Login")


# add quest to database form page
@app.route('/add_quest', methods=['GET', 'POST'])
def add_quest():
    trader_id_from_query = request.args.get('trader_id', type=int)
    form = Add_Quest(trader=trader_id_from_query)
    quest_images = 'app/static/images/quests/'
    traders = models.Trader.query.all()
    form.trader.choices = [(trader.id, trader.name) for trader in traders]
    if request.method == 'POST' and form.validate_on_submit():
        if "username" in session and session["username"] == "admin":
            image = request.files['image']
            if image and allowed_file(image.filename):
                imagename = secure_filename(form.image.data.filename)
                image.save(quest_images+imagename)
            else:
                file_error = "Wrong file type. Please upload a pdf, png, jpg, or jpeg."
                return render_template('add_quest.html', form=form, file_error=file_error, page_title="Add a Quest")
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
            login_error = "You are not logged in. Please log in."
            return render_template('add_quest.html', form=form, login_error=login_error, page_title="Add a Quest")
    else:
        return render_template('add_quest.html', form=form, page_title="Add a Quest")


# add trader to database form page
@app.route('/add_trader', methods=['GET', 'POST'])
def add_trader():
    form = Add_Trader()
    trader_images = 'app/static/images/traders/'
    if request.method == 'POST' and form.validate_on_submit():
        if "username" in session and session["username"] == "admin":
            image = request.files['image']
            if image and allowed_file(image.filename):
                imagename = secure_filename(form.image.data.filename)
                image.save(trader_images+imagename)
            else:
                file_error = "Wrong file type. Please upload a pdf, png, jpg, or jpeg."
                return render_template('add_trader.html', form=form, file_error=file_error, page_title="Add a Trader")
            new_trader = models.Trader()
            new_trader.name = form.name.data
            new_trader.desc = form.desc.data
            new_trader.image = imagename
            db.session.add(new_trader)
            db.session.commit()
            return redirect(url_for('trader', id=new_trader.id))
        else:
            login_error = "You are not logged in. Please log in."
            return render_template('add_trader.html', form=form, login_error=login_error, page_title="Add a Trader")
    else:
        return render_template('add_trader.html', form=form, page_title="Add a Trader")


# add location to database form page
@app.route('/add_location', methods=['GET', 'POST'])
def add_location():
    form = Add_Location()
    location_images = 'app/static/images/locations/'
    if request.method == 'POST' and form.validate_on_submit():
        if "username" in session and session["username"] == "admin":
            image = request.files['image']
            if image and allowed_file(image.filename):
                imagename = secure_filename(form.image.data.filename)
                image.save(location_images+imagename)
            else:
                file_error = "Wrong file type. Please upload a pdf, png, jpg, or jpeg."
                return render_template('add_location.html', form=form, file_error=file_error, page_title="Add a Location")
            map = request.files['map']
            if map and allowed_file(map.filename):
                mapname = secure_filename(form.map.data.filename)
                map.save(location_images+mapname)
            else:
                return render_template('add_location.html', form=form, page_title="Add a Location")
            new_location = models.Location()
            new_location.name = form.name.data
            new_location.desc = form.desc.data
            new_location.image = imagename
            new_location.map = mapname
            db.session.add(new_location)
            db.session.commit()
            return redirect(url_for('location', id=new_location.id))
        else:
            login_error = "You are not logged in. Please log in."
            return render_template('add_location.html', form=form, login_error=login_error, page_title="Add a Location")
    else:
        return render_template('add_location.html', form=form, page_title="Add a Location")


# add reward to a quest form page
@app.route('/add_reward', methods=['GET', 'POST'])
def add_reward():
    quest_id_from_query = request.args.get('quest_id', type=int)
    form = Add_Reward(quest=quest_id_from_query)
    quests = models.Quest.query.all()
    form.quest.choices = [(quest.id, quest.name) for quest in quests]
    if request.method == 'POST' and form.validate_on_submit():
        if "username" in session and session["username"] == "admin":
            new_reward = models.Reward()
            new_reward.item = form.item.data
            new_reward.quest = form.quest.data
            db.session.add(new_reward)
            db.session.commit()
            return redirect(url_for('quest', id=new_reward.quest))
        else:
            login_error = "You are not logged in. Please log in."
            return render_template('add_reward.html', form=form, login_error=login_error, page_title="Add a Reward")
    else:
        return render_template('add_reward.html', form=form, page_title="Add a Reward")


# add objective to a quest form page
@app.route('/add_objective', methods=['GET', 'POST'])
def add_objective():
    quest_id_from_query = request.args.get('quest_id', type=int)
    form = Add_Objective(quest=quest_id_from_query)
    quests = models.Quest.query.all()
    form.quest.choices = [(quest.id, quest.name) for quest in quests]
    if request.method == 'POST' and form.validate_on_submit():
        if "username" in session and session["username"] == "admin":
            new_objective = models.Objective()
            new_objective.desc = form.desc.data
            new_objective.quest = form.quest.data
            db.session.add(new_objective)
            db.session.commit()
            return redirect(url_for('quest', id=new_objective.quest))
        else:
            login_error = "You are not logged in. Please log in."
            return render_template('add_objective.html', form=form, login_error=login_error, page_title="Add an Objective")
    else:
        return render_template('add_objective.html', form=form, page_title="Add an Objective")


# add location to a quest form page
@app.route('/connect_location',  methods=['GET', 'POST'])
def connect_location():
    quest_id_from_query = request.args.get('quest_id', type=int)
    form = Connect_Location(quest=quest_id_from_query)
    quests = models.Quest.query.all()
    form.quest.choices = [(quest.id, quest.name) for quest in quests]
    locations = models.Location.query.all()
    form.location.choices = [(location.id, location.name) for location in locations]
    if request.method == 'POST' and form.validate_on_submit():
        if "username" in session and session["username"] == "admin":
            quest = models.Quest.query.filter_by(id=form.quest.data).first_or_404()
            location = models.Location.query.filter_by(id=form.location.data).first_or_404()
            quest.locations.append(location)
            db.session.add(quest)
            db.session.commit()
            return redirect(url_for('quest', id=quest.id))
        else:
            login_error = "You are not logged in. Please log in."
            return render_template('connect_location.html', form=form, login_error=login_error, page_title="Add a Location")
    else:
        return render_template('connect_location.html', form=form, page_title="Add a Location")


# add previous or subsequent quests to a quest form page
@app.route('/connect_quests',  methods=['GET', 'POST'])
def connect_quests():
    form = Connect_Quests()
    quests = models.Quest.query.all()
    form.previous.choices = [(quest.id, quest.name) for quest in quests]
    form.subsequent.choices = [(quest.id, quest.name) for quest in quests]
    if request.method == 'POST' and form.validate_on_submit():
        if "username" in session and session["username"] == "admin":
            previous = models.Quest.query.filter_by(id=form.previous.data).first_or_404()
            subsequent = models.Quest.query.filter_by(id=form.subsequent.data).first_or_404()
            previous.subsequent.append(subsequent)
            db.session.add(previous)
            db.session.commit()
            return redirect(url_for('quest', id=previous.id))
        else:
            login_error = "You are not logged in. Please log in."
            return render_template('connect_quests.html', form=form, login_error=login_error, page_title="Connect Quests")
    else:
        return render_template('connect_quests.html', form=form, page_title="Connect Quests")


# delete quest from database form page
@app.route('/delete_quest', methods=['GET', 'POST'])
def delete_quest():
    quest_id_from_query = request.args.get('quest_id', type=int)
    form = Delete_Quest(quest=quest_id_from_query)
    quests = models.Quest.query.all()
    form.quest.choices = [(quest.id, quest.name) for quest in quests]
    if request.method == 'POST' and form.validate_on_submit():
        if "username" in session and session["username"] == "admin":
            quest = db.session.query(models.Quest).filter(models.Quest.id == form.quest.data).first_or_404()
            db.session.delete(quest)
            db.session.commit()
            return redirect(url_for('quests'))
        else:
            login_error = "You are not logged in. Please log in."
            return render_template('delete_quests.html', form=form, login_error=login_error, page_title="Delete a Quest")
    else:
        return render_template('delete_quest.html', form=form, page_title="Delete a Quest")


# delete trader from database form page
@app.route('/delete_trader', methods=['GET', 'POST'])
def delete_trader():
    trader_id_from_query = request.args.get('trader_id', type=int)
    form = Delete_Trader(trader=trader_id_from_query)
    traders = models.Trader.query.all()
    form.trader.choices = [(trader.id, trader.name) for trader in traders]
    if request.method == 'POST' and form.validate_on_submit():
        if "username" in session and session["username"] == "admin":
            trader = db.session.query(models.Trader).filter(models.Trader.id == form.trader.data).first_or_404()
            db.session.delete(trader)
            db.session.commit()
            return redirect(url_for('traders'))
        else:
            login_error = "You are not logged in. Please log in."
            return render_template('delete_trader.html', form=form, login_error=login_error, page_title="Delete a Trader")
    else:
        return render_template('delete_trader.html', form=form, page_title="Delete a Trader")


# delete location from database form page
@app.route('/delete_location', methods=['GET', 'POST'])
def delete_location():
    location_id_from_query = request.args.get('location_id', type=int)
    form = Delete_Location(location=location_id_from_query)
    location = models.Location.query.all()
    form.location.choices = [(location.id, location.name) for location in location]
    if request.method == 'POST' and form.validate_on_submit():
        if "username" in session and session["username"] == "admin":
            location = db.session.query(models.Location).filter(models.Location.id == form.location.data).first_or_404()
            db.session.delete(location)
            db.session.commit()
            return redirect(url_for('locations'))
        else:
            login_error = "You are not logged in. Please log in."
            return render_template('delete_location.html', form=form, login_error=login_error, page_title="Delete a Location")
    else:
        return render_template('delete_location.html', form=form, page_title="Delete a Location")


# 404 error page
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')
