from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import os

# Initialize the database object
db = SQLAlchemy()

# Function to create and configure the Flask app
def create_app():
    app = Flask(__name__)

    # Load configuration settings from a separate config file
    app.config.from_object('app.config.Config')

    # Initialize the database with the Flask app
    db.init_app(app)

    # Set up Flask-Migrate for handling database migrations
    migrate = Migrate(app, db)

    # Import and register the main blueprint for routes
    from .routes.routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
