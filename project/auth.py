from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from .models import User
from . import db

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/signup')
def signup():
    return render_template('signup.html')

@auth.route('/editprofile')
@login_required
def edit_profile():
    return render_template('editprofile.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@auth.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    
    # determines if the user exists in the db by checking if this returns a user
    user = User.query.filter_by(email=email).first()

    if user: 
        flash('email address already exists')
        return redirect(url_for('auth.signup'))
    
    # otherwise, create a user 
    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))

    # add the user to the db 
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))

@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False 

    user = User.query.filter_by(email=email).first()

    # check if the user exists 
    if not user or not check_password_hash(user.password, password):
        flash('please check your login details and try again.')
        return redirect(url_for('auth.login'))
    
    # this goes through if the user exists + password was right
    login_user(user, remember=remember)
    return redirect(url_for('main.profile'))
    