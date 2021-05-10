from flask import render_template, flash, redirect, url_for
from flask_login import current_user, login_user, logout_user, login_required
from flask_mail import Message
from app import app, db, mail
from app.forms import LoginForm, RegistrationForm
from app.models import User, Reminder
from app.email import send_phone_verification
from app.tokens import generate_confirmation_token, confirm_token

from random import *
import datetime

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/user')
@login_required
def user():
    return render_template('user.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, phone_number=form.phone_number.data)
        user.set_password(form.password.data)
        newId = user.id
        db.session.add(user)
        db.session.commit()

        token = generate_confirmation_token(user.phone_number)
        confirm_url = url_for('confirm_phone_number', token=token, _external=True)
        send_phone_verification(form.phone_number.data, confirm_url)
        flash("You're registered! A verification link has been sent to your device.")
        return redirect(url_for('index'))

    return render_template('register.html', title='Register', form=form)

@app.route('/confirm/<token>')
@login_required
def confirm_phone_number(token):
    try:
        phone_number = confirm_token(token)
    except:
        flash('The confirmation link is invalid or has expired.')
    user = User.query.filter_by(phone_number=phone_number).first_or_404()
    if user.confirmed:
        flash('Account already confirmed. Please login.')
    else:
        user.active = True
        db.session.add(user)
        db.session.commit()
        flash('You have verified your account.')
    return redirect(url_for('index'))

# DEBUG, REMOVE BEFORE DEPLOYMENT
@app.route('/resetdb')
def resetdb():
    db.session.query(User).delete()
    db.session.query(Reminder).delete()
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/test')
def test():
    msg = Message("hello adam", sender="RemindMe", recipients=["5854558650@vtext.com"])
    mail.send(msg)
    return redirect(url_for('index'))
