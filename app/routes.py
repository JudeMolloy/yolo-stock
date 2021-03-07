import stripe

from flask import url_for, redirect, render_template, flash, jsonify, request
from app import app, plaid_client
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Order
from app.forms import LoginForm, CreateAccountForm
from config import Config
from randomstock import get_ticket_array, get_stock
from apiscript import OrderAPI
from update_tickers import run

DOMAIN = Config.DOMAIN
stripe.api_key = Config.STRIPE_SECRET_KEY


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
    user = User.query.filter_by(id=current_user.id).first_or_404()
    bank_balance = user.bank_balance
    print(bank_balance)
    if request.method == "POST":
        data = request.form
        amount = data['amount']
        stock_name = data['stock-name']
        price = data['price']
        stock_array = get()
        ticker_prices = get_ticket_array(stock_array, amount, OrderAPI("apikey", "demoaccount20212", "apipass"))
        stock_to_buy = get_stock(ticker_prices)
        order = Order(stock_name=stock_name, amount=amount, user_id=current_user.id)
        order.save_to_db()

    return render_template("start.html", bank_balance=bank_balance)


@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():

    # Fetch most recent order for account
    order = Order.query.filter_by(user_id=current_user.id).order_by(Order.datetime.desc()).first()
    amount = order.amount
    stock_name = order.stock_name


    success_url = DOMAIN + url_for('payment_success')
    cancel_url = DOMAIN + url_for('payment_cancel')
    session = stripe.checkout.Session.create(
    payment_method_types=['card'],
    line_items=[{
      'price_data': {
        'currency': 'GBP',
        'product_data': {
          'name': stock_name,
        },
        'unit_amount': amount,
      },
      'quantity': 1,
    }],
    mode='payment',
    success_url=success_url,
    cancel_url=cancel_url,
    )

    return jsonify(id=session.id)


@app.route('/payment-success')
def payment_success():
    return "Successful Payment"


@app.route('/payment-cancel')
def payment_cancel():
    return "Cancel Payment"


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

    print(accounts[0]['balances']['available'])
    available = accounts[0]['balances']['available']
    user = User.query.filter_by(id=current_user.id).first()
    if user:
        user.bank_balance = available
        user.save_to_db()
    return redirect(url_for('start'))


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
        return redirect(url_for('link_bank'))
    return render_template('login.html', form=form)


@app.route("/dashboard")
def dashboard():
    return render_template('dashboard.html')


@app.route("/done")
def done():
    return render_template('done.html')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))