from flask import render_template, redirect, url_for, flash, jsonify, request
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from . import db, login_manager  # Changed to relative import
from .models import User
from .forms import SignupForm, SigninForm
from flask import Blueprint
import random

main_bp = Blueprint('main', __name__)
auth_bp = Blueprint('auth', __name__)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@main_bp.route('/')
def home():
    return render_template('index.html')

@main_bp.route('/api/stations')
def api_stations():
    stations = generate_random_stations(15)
    return jsonify([{
        'number': s['number'],
        'name': s['name'],
        'position': s['position'],
        'bikes': s['available_bikes'],
        'stands': s['available_bike_stands'],
        'address': s['address'],
        'capacity': s['capacity']
    } for s in stations])

@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    
    form = SignupForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash('Email already exists', 'danger')
            return redirect(url_for('auth.signup'))
        
        new_user = User(
            email=form.email.data,
            password=generate_password_hash(form.password.data)
        )
        db.session.add(new_user)
        db.session.commit()
        
        flash('Account created! Please login', 'success')
        return redirect(url_for('auth.signin'))
    
    return render_template('signup.html', form=form)

@auth_bp.route('/signin', methods=['GET', 'POST'])
def signin():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    
    form = SigninForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('main.home'))
        flash('Invalid email or password', 'danger')
    return render_template('signin.html', form=form)

@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))

def generate_random_stations(num_stations):
    street_names = ["Main", "Oak", "Pine", "Maple", "Cedar", "Elm", "Birch", "Spruce"]
    stations = []
    for i in range(num_stations):
        stations.append({
            'number': i + 1,
            'name': f"{random.choice(street_names)} Station",
            'position': {
                'lat': 53.3498 + random.uniform(-0.02, 0.02),
                'lng': -6.2603 + random.uniform(-0.02, 0.02)
            },
            'available_bikes': random.randint(0, 20),
            'available_bike_stands': random.randint(0, 20),
            'address': f"{random.randint(1, 200)} {random.choice(street_names)} Street",
            'capacity': 20
        })
    return stations