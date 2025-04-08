from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from .models import db, User
from .forms import SignupForm, LoginForm

# Blueprint for Authentication
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/signup', methods=['GET', 'POST'])
@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = SignupForm()

    if form.validate_on_submit():
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash('Account already exists', 'danger')
        else:
            new_user = User(
                email=form.email.data,
                password=generate_password_hash(form.password.data)
            )
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful! You are now redirected to the homepage.', 'success')
            # Redirect to the index page
            return redirect(url_for('main.index'))

    return render_template('signup.html', form=form)

@auth_bp.route('/login', methods=['GET', 'POST'])
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))  # Redirect to index if the user is already logged in

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('main.index'))  # Redirect to index after successful login
        else:
            flash('Invalid email or password', 'danger')

    return render_template('login.html', form=form)
from flask_login import logout_user

@auth_bp.route('/logout')
def logout():
    logout_user()  # This will log the user out
    return redirect(url_for('main.index'))  # Redirect to index page after logging out



# Blueprint for Main (Index Page)
main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html')  # Make sure index.html exists in your templates
