from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager
import os

# Initialize the database object
db = SQLAlchemy()

# Function to create and configure the Flask app
def create_app():
    app = Flask(__name__)

    # Load environment variables from .env file
    load_dotenv()

    # Load configuration settings from a separate config file
    app.config.from_object('app.config.Config')

    # Initialize the database with the Flask app
    db.init_app(app)

    # Set up Flask-Migrate for handling database migrations
    Migrate(app, db)

    # Initialize JWT
    jwt = JWTManager(app)

    # Import and register the main blueprint for routes
    from .routes.routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # Import and register auth blueprint for authentication routes
    from .routes.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # Import and register transactions blueprint for transaction routes
    from .routes.transactions import transactions as transactions_blueprint
    app.register_blueprint(transactions_blueprint)

    return app
