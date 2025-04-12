from flask import Flask
from flask_login import LoginManager
from .models import db, User
from .routes import auth_bp, main_bp
from .jcdecaux_collector import start_scheduler
from .routes import predict_bp
start_scheduler()
from flask import Flask, request, jsonify
import pandas as pd
import joblib
from .routes import recommend_bp
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your_secret_key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your_database.db'  # Use your actual database URI
    
    db.init_app(app)
    login_manager.init_app(app)

    # Define the user_loader function
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))  # Loads the user from the database based on user_id

    # Register Blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(main_bp)
    app.register_blueprint(predict_bp)
    app.register_blueprint(recommend_bp)

    model = joblib.load('instance/bike_predictor.pkl')

    @app.route('/predict_bikes', methods=['GET'])
    def predict_bikes():
        try:
            station_id = int(request.args.get('station_id'))
            day = request.args.get('day')
            hour = int(request.args.get('hour'))

            input_df = pd.DataFrame([{
                'station_id': station_id,
                'day': day,
                'hour': hour
            }])

            prediction = model.predict(input_df)[0]

            return jsonify({
                'station_id': station_id,
                'day': day,
                'hour': hour,
                'predicted_bikes': int(round(prediction))
            })
        except Exception as e:
            return jsonify({'error': str(e)})

      # Starts background data fetch
    return app

  