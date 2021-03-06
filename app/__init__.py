import os

import plaid

from flask import Flask

from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Login
login = LoginManager(app)
login.login_view = 'login'

PLAID_CLIENT_ID = os.getenv('PLAID_CLIENT_ID')
print(PLAID_CLIENT_ID)

print(Config.PLAID_CLIENT_ID)
print(Config.PLAID_SECRET)
print(Config.PLAID_ENV)

plaid_client = plaid.Client(client_id=Config.PLAID_CLIENT_ID,
                      secret=Config.PLAID_SECRET,
                      environment=Config.PLAID_ENV)


from app import routes, models