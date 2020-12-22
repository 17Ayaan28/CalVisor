from app import db, login_manager
from flask import current_app
from flask_login import UserMixin
from datetime import datetime, date

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password = db.Column(db.String(128))
    profile_settings = db.Column(db.Boolean, default = False)

    events = db.relationship('Event')
    # location = db.relationship('Location')

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

class Event(db.Model):
    __tablename__ = 'events'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    addr = db.Column(db.String(128))
    date = db.Column(db.Date)
    start_time = db.Column(db.Time)
    end_time = db.Column(db.Time)
    repeating_event = db.Column(db.Boolean, default = False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    invites = db.relationship('Invites')

class Invites(db.Model): #Invitation System
    __tablename__ = 'invites'

    id = db.Column(db.Integer, primary_key=True)
    inviter_id = db.Column(db.Integer)
    invitee_id = db.Column(db.Integer)
    invitee_username = db.Column(db.String(128))
    invite_accepted = db.Column(db.Boolean, default = False)
    invite_rejected = db.Column(db.Boolean, default = False)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))

    scheduling = db.relationship('Scheduling_Invites')

class Accepted_Inviters (db.Model): #Invitation System
    __tablename__ = 'accepted_inviters'

    id = db.Column(db.Integer, primary_key=True)
    invitee_id = db.Column(db.Integer)
    inviter_id = db.Column(db.Integer)
    invitee_username = db.Column(db.String(128))
    inviter_username = db.Column(db.String(128))

class Scheduling_Invites (db.Model): #Invitation System
    __tablename__ = 'scheduling_invites'

    id = db.Column(db.Integer, primary_key=True)
    invite_id = db.Column(db.Integer, db.ForeignKey('invites.id'))
    inviter_id = db.Column(db.Integer)
    invitee_id = db.Column(db.Integer)
    inviter_username = db.Column(db.String(128))
    invitee_username = db.Column(db.String(128))
    # invite_date = db.Column(db.Date)
    # invite_time = db.Column(db.Time)
    invite_name = db.Column(db.String(64))
    invite_location_addr = db.Column(db.String(128), default="")
    # invite_duration = db.Column(db.Integer, default=0)
    invite_date = db.Column(db.Date)
    invite_start_time = db.Column(db.Time)
    invite_end_time = db.Column(db.Time)

    invitee_next_event = db.Column(db.Integer)
    invitee_previous_event = db.Column(db.Integer)
    # invite_search_time = db.Column(db.Integer, default=0)
    invitee_approval = db.Column(db.Boolean, default=False)
    inviter_approval = db.Column(db.Boolean, default=False)
    denied_date = db.Column(db.String(128), default=datetime.now().strftime("%d/%m/%Y"))
    denied_time= db.Column(db.String(128), default=datetime.now().strftime("%H:%M:%S"))
