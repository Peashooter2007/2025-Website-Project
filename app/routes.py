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
    print(quest, quest.name)
    return render_template('quest.html', quest=quest)   


@app.errorhandler(404)
def page_not_found(e):
    return('sum ting wong')



