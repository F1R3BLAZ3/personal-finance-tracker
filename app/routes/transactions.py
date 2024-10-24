from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models import db, FinancialTransaction
from ..services.plaid_service import get_transactions

transactions = Blueprint('transactions', __name__)

@transactions.route('/transactions', methods=['GET'])
@jwt_required()
def transactions():
    access_token = request.headers.get('Authorization').split(" ")[1]  # Assuming Bearer token
    start_date = request.args.get('start_date')  # Format: YYYY-MM-DD
    end_date = request.args.get('end_date')      # Format: YYYY-MM-DD

    transactions = get_transactions(access_token, start_date, end_date)
    return jsonify({'transactions': transactions})
