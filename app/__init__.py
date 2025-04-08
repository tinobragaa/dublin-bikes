from flask import Flask
from flask_login import LoginManager
from .models import db, User
from .routes import auth_bp, main_bp

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

    return app
    
