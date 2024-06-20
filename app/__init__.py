from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Initialize SQLAlchemy
db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    # Configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project_2.db'
    app.config['SECRET_KEY'] = 'your_secret_key'  # We'll generate this in app.py

    db.init_app(app)

    # Import and register the blueprint from routes.py
    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app

