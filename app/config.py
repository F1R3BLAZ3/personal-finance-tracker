import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
    f'sqlite:///{os.path.join(basedir, "instance", "personal_finance_tracker.db")}'
    SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS') == 'True'
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    PLAID_CLIENT_ID = os.environ.get("PLAID_CLIENT_ID")
    PLAID_SECRET = os.environ.get("PLAID_SECRET")
    PLAID_ENV = os.environ.get("PLAID_ENV")
