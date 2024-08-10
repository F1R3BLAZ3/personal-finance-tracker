from flask import Blueprint, request, jsonify
from ..models import db, User, Transaction, Budget

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return "Welcome to the Personal Finance Tracker API"

# Add routes for authentication, budgets, transactions, etc.
