# tests/test_app.py
import os
import sys
import tempfile
import json
import pytest
import numpy as np
import pandas as pd

# Ensure the project root is in sys.path:
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Monkey-patch joblib.load to return a dummy model for predict_bikes endpoint
class DummyModel:
    def predict(self, X):
        # Return an array with a constant value (e.g., 5) for each row
        return np.array([5] * len(X))

@pytest.fixture
def app():
    # Create a temporary SQLite database file
    db_fd, db_path = tempfile.mkstemp()
    # Import and create the app using your Flask factory function
    from app import create_app
    test_config = {
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///' + db_path,
        'SECRET_KEY': 'test_secret_key',
        'WTF_CSRF_ENABLED': False
    }
    app = create_app()
    app.config.update(test_config)

    # Create database tables
    with app.app_context():
        from app.models import db
        db.create_all()
    yield app

    os.close(db_fd)
    os.unlink(db_path)

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture(autouse=True)
def override_model(monkeypatch):
    # Override joblib.load to use DummyModel so /predict_bikes works consistently
    import joblib
    monkeypatch.setattr(joblib, "load", lambda filename: DummyModel())

# 1. Test the index (main) route.
def test_index(client):
    response = client.get('/')
    assert response.status_code == 200
    # Check for a keyword assumed in your index template (e.g., "Dublin Bikes")
    assert b'Dublin Bikes' in response.data

# 2. Test the signup page (GET) from the auth blueprint.
def test_signup_get(client):
    response = client.get('/auth/signup')
    assert response.status_code == 200
    assert b'CREATE ACCOUNT' in response.data

# 3. Test signup (POST) with an invalid email (not ending with @gmail.com).
def test_signup_invalid_email(client):
    data = {
        'email': 'user@yahoo.com',  # Invalid: must end with @gmail.com
        'password': '1234',
        'confirm': '1234',
    }
    response = client.post('/auth/signup', data=data, follow_redirects=True)
    # Assuming the WTForms validator error message is rendered in the response.
    assert b'Please enter a valid Gmail address' in response.data

# 4. Test signup (POST) with a valid email.
def test_signup_valid(client):
    data = {
        'email': 'user@gmail.com',  # Valid email
        'password': '1234',
        'confirm': '1234',
    }
    response = client.post('/auth/signup', data=data, follow_redirects=True)
    # On success, the user should be redirected (and a success message flashed)
    assert b'Registration successful' in response.data or b'Welcome' in response.data

# 5. Test the predict_bikes API endpoint.
def test_predict_bikes(client):
    response = client.get('/predict_bikes?station_id=1&day=Monday&hour=10')
    assert response.status_code == 200
    data = json.loads(response.data)
    # With DummyModel, predicted_bikes should be 5.
    assert data.get('predicted_bikes') == 5
    assert data.get('station_id') == 1
    # Also check the keys exist.
    assert 'day' in data and 'hour' in data

# 6. Test the recommend_stations API endpoint.
def test_recommend_stations(monkeypatch, client):
    # Create a dummy DataFrame to simulate combined station data.
    df_dummy = pd.DataFrame({
        'station_id': [1, 2, 3, 4],
        'name': ['Station 1', 'Station 2', 'Station 3', 'Station 4'],
        'lat': [53.3498, 53.3500, 53.3502, 53.3496],
        'lng': [-6.2603, -6.2601, -6.2605, -6.2600],
        'bikes_available': [0, 5, 3, 2],
        'stands_available': [10, 5, 7, 8],
        'timestamp': ['2021-01-01 12:00:00']*4
    })

    # Monkey-patch pd.read_csv so that recommend_stations reads our dummy data.
    monkeypatch.setattr(pd, 'read_csv', lambda filename: df_dummy)

    response = client.get('/recommend_stations?station_id=1&condition=need_bikes')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'recommendations' in data
    # Ensure we received a list (and at least one recommendation given dummy data).
    assert isinstance(data['recommendations'], list)
    assert len(data['recommendations']) > 0

# 7. Test the login page (GET) from the auth blueprint.
def test_login_get(client):
    response = client.get('/auth/login')
    assert response.status_code == 200
    assert b'Login' in response.data

# 8. Test logout functionality.
def test_logout(client, app):
    # First, register a user so login can work.
    with app.app_context():
        from app.models import db, User
        from werkzeug.security import generate_password_hash
        test_user = User(email="test@gmail.com", password=generate_password_hash("1234"))
        db.session.add(test_user)
        db.session.commit()

    # Login with the test user.
    login_response = client.post('/auth/login', data={
        'email': 'test@gmail.com',
        'password': '1234'
    }, follow_redirects=True)
    # A successful login often redirects, so check for a logout button or similar indicator.
    assert b'Logout' in login_response.data or login_response.status_code == 200

    # Now log out.
    logout_response = client.get('/auth/logout', follow_redirects=True)
    assert logout_response.status_code == 200
    # Check that after logout, a login link or similar is visible.
    assert b'Login' in logout_response.data
