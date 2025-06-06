from app.routes import db


QuestLocation = db.Table('QuestLocation',
    db.Column('qid', db.Integer, db.ForeignKey('Quest.id')),
    db.Column('lid', db.Integer, db.ForeignKey('Location.id'))
)

QuestObjective = db.Table('QuestObjective',
    db.Column('qid', db.Integer, db.ForeignKey('Quest.id')),
    db.Column('oid', db.Integer, db.ForeignKey('Objective.id'))
)

QuestRep = db.Table('QuestRep',
    db.Column('qid', db.Integer, db.ForeignKey('Quest.id')),
    db.Column('rid', db.Integer, db.ForeignKey('Rep.id'))
)


Order = db.Table('Order',
    db.Column('previous', db.Integer, db.ForeignKey('Quest.id')),
    db.Column('subsequent', db.Integer, db.ForeignKey('Quest.id'))
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

    trader_name = db.relationship('Trader', back_populates = 'quests')

    rewards = db.relationship('Reward', back_populates = 'quest_name')

    locations = db.relationship('Location', secondary = QuestLocation, back_populates = 'quests')

    rep = db.relationship('Rep', secondary = QuestRep, back_populates = 'quests')

    objectives = db.relationship('Objective', secondary = QuestObjective, back_populates = 'quests')

    subsequent = db.relationship('Quest', secondary = Order, primaryjoin = (Order.c.previous == id), secondaryjoin = (Order.c.subsequent == id), back_populates = 'previous')

    previous = db.relationship('Quest', secondary = Order, primaryjoin = (Order.c.subsequent == id), secondaryjoin = (Order.c.previous == id), back_populates = 'subsequent')

    def __repr__(self):
        return self.name 


class Location(db.Model):
    __tablename__ = 'Location'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text())    
    desc = db.Column(db.Text())
    image = db.Column(db.Text())
    map = db.Column(db.Text())
    
    quests = db.relationship('Quest', secondary = QuestLocation, back_populates = 'locations')

    def __repr__(self):
        return self.name 


class Objective(db.Model):
    __tablename__ = 'Objective'
    id = db.Column(db.Integer, primary_key=True) 
    desc = db.Column(db.Text())

    quests = db.relationship('Quest', secondary = QuestObjective, back_populates = 'objectives')


class Rep(db.Model):
    __tablename__ = 'Rep'
    id = db.Column(db.Integer, primary_key=True) 
    rep = db.Column(db.Text())

    quests = db.relationship('Quest', secondary = QuestRep, back_populates = 'rep')

class Reward(db.Model):
    __tablename__ = 'Reward'
    id = db.Column(db.Integer, primary_key=True) 
    item = db.Column(db.Text())
    quest = db.Column(db.Integer, db.ForeignKey('Quest.id'))

    quest_name = db.relationship('Quest', back_populates = 'rewards')

class Trader(db.Model):
    __tablename__ = 'Trader'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text())    
    desc = db.Column(db.Text())
    image = db.Column(db.Text())
    
    quests = db.relationship('Quest', back_populates = 'trader_name')

    def __repr__(self):
        return self.name 
