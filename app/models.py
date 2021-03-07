import datetime as datetime

from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login
from datetime import datetime


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), index=True, unique=True)
    email = db.Column(db.String(128), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    bank_balance = db.Column(db.Float(), server_default="0")
    orders = db.relationship('Order', backref='user', lazy=True)
    #plaid_access_token = db.Column(db.String)

    def __init__(self, username):
        self.username = username

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    stock_name = db.Column(db.String(16), nullable=False)
    amount = db.Column(db.Float(), nullable=False)
    datetime = db.Column(db.DateTime, default=datetime.now())
    #active = db.Column(db.Boolean)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self, stock_name, amount, user_id):
        self.stock_name = stock_name
        self.amount = amount
        self.user_id = user_id

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
