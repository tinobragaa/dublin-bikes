from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from .models import db, User
from .forms import SignupForm, LoginForm
from flask import Blueprint, request, jsonify
import joblib
import pandas as pd
import math
import numpy as np
import pandas as pd

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
predict_bp = Blueprint('predict', __name__)

# Load the trained model
model = joblib.load('instance/bike_predictor.pkl')

@predict_bp.route('/predict_bikes', methods=['GET'])
def predict_bikes():
    try:
        station_id = int(request.args.get('station_id'))
        day = request.args.get('day')  # Ex: "Monday"
        hour = int(request.args.get('hour'))  # Ex: 14

        # Input as DataFrame
        input_df = pd.DataFrame([{
            'station_id': station_id,
            'day': day,
            'hour': hour
        }])

        # Predict
        prediction = model.predict(input_df)[0]

        return jsonify({
            'station_id': station_id,
            'day': day,
            'hour': hour,
            'predicted_bikes': int(round(prediction))
        })

    except Exception as e:
        return jsonify({'error': str(e)})
recommend_bp = Blueprint('recommend', __name__)

def haversine(lat1, lon1, lat2, lon2):
    """Compute the haversine distance between two (lat, lng) pairs in kilometers."""
    R = 6371.0  # Earth's radius in km
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c
@recommend_bp.route('/recommend_stations', methods=['GET'])
def recommend_stations():
    try:
        # Get the target station id and condition
        station_id = int(request.args.get('station_id'))
        condition = request.args.get('condition')  # e.g., "need_bikes" or "need_stands"
        
        # Read the combined station CSV which includes lat and lng
        df = pd.read_csv("instance/combined_station_data.csv")
        
        # Group by station_id and select the most recent entry (assuming timestamp is sortable)
        df_latest = df.sort_values(by="timestamp").groupby("station_id", as_index=False).tail(1)
        
        # Find the target station row
        target_rows = df_latest[df_latest['station_id'] == station_id]
        if target_rows.empty:
            return jsonify({'error': 'Target station not found'}), 404
        target = target_rows.iloc[0]
        target_lat = target['lat']
        target_lng = target['lng']
        
        # Get candidate stations (exclude the target)
        candidates = df_latest[df_latest['station_id'] != station_id]
        
        # Filter candidates by condition:
        if condition == "need_bikes":
            filtered_candidates = candidates[candidates['bikes_available'] > 0]
        elif condition == "need_stands":
            filtered_candidates = candidates[candidates['stands_available'] > 0]
        else:
            filtered_candidates = candidates
        
        # If no candidate meets the condition, fall back to the full candidate set
        if filtered_candidates.empty:
            filtered_candidates = candidates
        
        # Compute distance for each candidate using the haversine function
        filtered_candidates = filtered_candidates.copy()  # avoid SettingWithCopyWarning
        filtered_candidates['distance_km'] = filtered_candidates.apply(
            lambda row: haversine(target_lat, target_lng, row['lat'], row['lng']), axis=1
        )
        
        # Sort by distance (nearest first)
        filtered_candidates_sorted = filtered_candidates.sort_values(by='distance_km')
        
        # Select the top 3 recommendations
        recommendations = filtered_candidates_sorted.head(3)[[
            'station_id', 'name', 'lat', 'lng', 'bikes_available', 'stands_available', 'distance_km'
        ]].to_dict(orient='records')
        
        return jsonify({'recommendations': recommendations})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
