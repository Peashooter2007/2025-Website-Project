from app.routes import db


QuestLocation = db.Table('QuestLocation',
    db.Column('qid', db.Integer, db.ForeignKey('Quest.id')),
    db.Column('lid', db.Integer, db.ForeignKey('Location.id'))
)

QuestObjective = db.Table('QuestObjective',
    db.Column('qid', db.Integer, db.ForeignKey('Quest.id')),
    db.Column('oid', db.Integer, db.ForeignKey('Objective.id'))
)


QuestReward = db.Table('QuestReward',
    db.Column('qid', db.Integer, db.ForeignKey('Quest.id')),
    db.Column('rid', db.Integer, db.ForeignKey('Reward.id'))
)


class Quest(db.Model):
    __tablename__ = 'Quest'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text())    
    desc = db.Column(db.Text())
    lvl = db.Column(db.Integer())
    exp = db.Column(db.Integer())
    image = db.Column(db.Text())
    trader = db.Column(db.Integer, db.ForeignKey('Trader.id'))

    trader_name = db.relationship('Trader', backref='quests_given_by_this_trader')

    location = db.relationship('Location', secondary = QuestLocation, back_populates = 'quests')

    objective = db.relationship('Objective', secondary = QuestObjective, back_populates = 'quests')

    reward = db.relationship('Reward', secondary = QuestReward, back_populates = 'quests')

    def __repr__(self):
        return self.name 


class Location(db.Model):
    __tablename__ = 'Location'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text())    
    desc = db.Column(db.Text())
    image = db.Column(db.Text())
    map = db.Column(db.Text())

    quest = db.relationship('Quest', secondary = QuestLocation, back_populates = 'locations')

    def __repr__(self):
        return self.name 


class Objective(db.model):
    id = db.Column(db.Integer, primary_key=True) 
    desc = db.Column(db.Text())
    quest = db.relationship('Quest', secondary = QuestObjective, back_populates = 'objectives')


class Reward(db.model):
    __tablename__ = 'Reward'
    id = db.Column(db.Integer, primary_key=True) 
    item = db.Column(db.Text())
    quest = db.relationship('Quest', secondary = QuestReward, back_populates = 'rewards')


class Trader(db.model):
    __tablename__ = 'Trader'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text())    
    desc = db.Column(db.Text())
    image = db.Column(db.Text())
