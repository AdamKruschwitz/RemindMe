from app import db, login
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64))
    phone_number = db.Column(db.String(10), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    reminders = db.relationship('Reminder', backref='owner', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)

class Reminder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(160))
    date_to_send = db.Column(db.DateTime, default=datetime.utcnow)
    date_last_sent = db.Column(db.DateTime)
    user_id = db.column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Reminder {}>'.format(self.text)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))
