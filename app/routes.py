from flask import url_for, redirect, render_template, flash, jsonify, request
from app import app, plaid_client
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User
from app.forms import LoginForm, CreateAccountForm
from config import Config

IBAN = Config.IBAN
ADDRESS = Config.ADDRESS
RECIPIENT_NAME = Config.RECIPIENT_NAME
BACS = Config.BACS
REFERENCE = Config.REFERENCE

access_token = None
public_token = None


@app.route('/')
def index():
    return "Welcome to YOLO! Creating risk where there isn't any since 2021."


@app.route('/link-bank')
@login_required
def link_bank():
    return render_template('link-bank.html')


@app.route('/start')
@login_required
def start():
    if request.method == "POST":

        recipient_response = plaid_client.PaymentInitiation.create_recipient(
            RECIPIENT_NAME,
            None,  # IBAN
            None,  # Address
            bacs = BACS
        )
        recipient_id = recipient_response["recipient_id"]

        data = request.form
        amount = data['amount']
        payment_response = plaid_client.PaymentInitiation.create_payment(
            recipient_id,
            REFERENCE,
            amount
        )
        payment_id = payment_response["payment_id"]
        status = payment_response["status"]


@app.route("/get_access_token", methods=['POST'])
@login_required
def get_access_token():
    global access_token
    public_token = request.form['public_token']
    exchange_response = \
        plaid_client.Item.public_token.exchange(public_token)
    print('access token: ' + exchange_response['access_token'])
    print('item ID: ' + exchange_response['item_id'])
    access_token = exchange_response['access_token']
    response = plaid_client.Accounts.balance.get(access_token)
    accounts = response['accounts']
    print(accounts)
    return jsonify(accounts)


@app.route("/create-link-token-balance", methods=['POST'])
@login_required
def create_link_token_balance():
    # Get the client_user_id by searching for the current user
    plaid_client_user_id = str(current_user.id)
    print(plaid_client_user_id)
    # Create a link_token for the given user
    response = plaid_client.LinkToken.create({
      'user': {
        'client_user_id': plaid_client_user_id,
      },
      'products': ['auth'],
      'client_name': 'YOLO',
      'country_codes': ['GB'],
      'language': 'en',
      'webhook': 'https://webhook.sample.com',
    })
    link_token = response['link_token']
    # Send the data to the client
    return jsonify(response)


@app.route("/create-link-token-payment", methods=['POST'])
def create_link_token_payment():
    # Get the client_user_id by searching for the current user
    plaid_client_user_id = str(current_user.id)
    # Create a link_token for the given user
    response = plaid_client.LinkToken.create({
      'user': {
        'client_user_id': plaid_client_user_id,
      },
      'products': ['payment_initiation'],
      'client_name': 'My App',
      'country_codes': ['GB'],
      'language': 'en',
      'webhook': 'https://webhook.sample.com',
      'payment_initiation': {
        'payment_id': plaid_payment_id,
      }
    })
    link_token = response['link_token']
    # Send the data to the client
    return jsonify(response)


@app.route('/create-account', methods=['GET', 'POST'])
def create_account():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = CreateAccountForm()
    if form.validate_on_submit():
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        user.save_to_db()
        flash('Account Creation successful')
        return redirect(url_for('login'))
    return render_template('create-account.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', form=form)

@app.route("/dashboard")
def dashboard():
    return render_template('dashboard.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))