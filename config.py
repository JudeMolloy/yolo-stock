import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'VERY DIFFICULT TO GUESS OK?'

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    PLAID_CLIENT_ID = os.getenv('PLAID_CLIENT_ID')
    PLAID_SECRET = os.getenv('PLAID_SECRET')
    PLAID_PUBLIC_KEY = os.getenv('PLAID_PUBLIC_KEY')

    PLAID_ENV = os.getenv('PLAID_ENV', 'sandbox')

    STRIPE_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY')

    IG_API_KEY = os.getenv('IG_API_KEY')
    IG_API_USERNAME = os.getenv('IG_API_USERNAME')
    IG_API_PASSWORD = os.getenv('IG_API_PASSWORD')

    IBAN = os.getenv('IBAN')
    ADDRESS = os.getenv('ADDRESS')
    BACS = os.getenv('BACS')
    RECIPIENT_NAME = os.getenv('RECIPIENT_NAME', 'YOLO')
    REFERENCE = os.getenv('REFERENCE', 'YOLO Payment')

    DOMAIN = os.getenv('DOMAIN', 'http://127.0.0.1:5000/')
