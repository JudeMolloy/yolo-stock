from flask import url_for, redirect, render_template, flash, jsonify
from app import app, plaid_client
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User
from app.forms import LoginForm, CreateAccountForm


@app.route('/')
def index():
    return "Hello, World!"


@app.route('/link-bank')
@login_required
def link_bank():
    return render_template('link-bank.html')


@app.route("/create_link_token", methods=['POST'])
@login_required
def create_link_token():
    # Get the client_user_id by searching for the current user
    plaid_client_user_id = current_user.id
    print(plaid_client_user_id)
    # Create a link_token for the given user
    response = plaid_client.LinkToken.create({
      'user': {
        'client_user_id': plaid_client_user_id,
      },
      'products': ['balance'],
      'client_name': 'YOLO',
      'country_codes': ['UK'],
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
        return redirect(url_for('index'))
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))