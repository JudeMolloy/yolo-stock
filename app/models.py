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
    bank_balance = db.Float()
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
    amount = db.Column(db.Integer, nullable=False)
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

        [{'account_id': 'KjGrwAB36RHe3QWWE9ygtmn8WNJMneT6d89er',
          'balances': {'available': 100, 'current': 110, 'iso_currency_code': 'GBP', 'limit': None,
                       'unofficial_currency_code': None}, 'mask': '0000', 'name': 'Plaid Checking',
          'official_name': 'Plaid Gold Standard 0% Interest Checking', 'subtype': 'checking', 'type': 'depository'},
         {'account_id': 'rlA4X7QN1qh4rNmmeWdRs6DeqAkaD9fy8wAjB',
          'balances': {'available': 200, 'current': 210, 'iso_currency_code': 'GBP', 'limit': None,
                       'unofficial_currency_code': None}, 'mask': '1111', 'name': 'Plaid Saving',
          'official_name': 'Plaid Silver Standard 0.1% Interest Saving', 'subtype': 'savings', 'type': 'depository'},
         {'account_id': 'zdREBl8oVJIvNpLLqGxeuky5oMwaydsEkayRJ',
          'balances': {'available': None, 'current': 1000, 'iso_currency_code': 'GBP', 'limit': None,
                       'unofficial_currency_code': None}, 'mask': '2222', 'name': 'Plaid CD',
          'official_name': 'Plaid Bronze Standard 0.2% Interest CD', 'subtype': 'cd', 'type': 'depository'},
         {'account_id': 'Bz1gNL8yAwIJpxwwBXynIKWJwonDWxH7mypd9',
          'balances': {'available': None, 'current': 410, 'iso_currency_code': 'GBP', 'limit': 2000,
                       'unofficial_currency_code': None}, 'mask': '3333', 'name': 'Plaid Credit Card',
          'official_name': 'Plaid Diamond 12.5% APR Interest Credit Card', 'subtype': 'credit card', 'type': 'credit'},
         {'account_id': '3ezDVnakoPTPLJjjBp4AtMy4dDZzyBfw4Jjkd',
          'balances': {'available': 43200, 'current': 43200, 'iso_currency_code': 'GBP', 'limit': None,
                       'unofficial_currency_code': None}, 'mask': '4444', 'name': 'Plaid Money Market',
          'official_name': 'Plaid Platinum Standard 1.85% Interest Money Market', 'subtype': 'money market',
          'type': 'depository'}, {'account_id': 'x39ZLDokyxilNpyywkL8UVp3QGaJpxc9rwzxr',
                                  'balances': {'available': None, 'current': 320.76, 'iso_currency_code': 'GBP',
                                               'limit': None, 'unofficial_currency_code': None}, 'mask': '5555',
                                  'name': 'Plaid IRA', 'official_name': None, 'subtype': 'ira', 'type': 'investment'},
         {'account_id': 'dPjAeMK7Bghd1aeejLxZInpMazVDpxfPVNbvg',
          'balances': {'available': None, 'current': 23631.9805, 'iso_currency_code': 'GBP', 'limit': None,
                       'unofficial_currency_code': None}, 'mask': '6666', 'name': 'Plaid 401k', 'official_name': None,
          'subtype': '401k', 'type': 'investment'}, {'account_id': 'aa4LJ6ANKkIZ1344mbz6una5bRX1ayfRy4Erg',
                                                     'balances': {'available': None, 'current': 65262,
                                                                  'iso_currency_code': 'GBP', 'limit': None,
                                                                  'unofficial_currency_code': None}, 'mask': '7777',
                                                     'name': 'Plaid Student Loan', 'official_name': None,
                                                     'subtype': 'student', 'type': 'loan'},
         {'account_id': '4QBgwn4yD6fk4n99jmNDf1yRnVNByaCgG5vBX',
          'balances': {'available': None, 'current': 56302.06, 'iso_currency_code': 'GBP', 'limit': None,
                       'unofficial_currency_code': None}, 'mask': '8888', 'name': 'Plaid Mortgage',
          'official_name': None, 'subtype': 'mortgage', 'type': 'loan'}]