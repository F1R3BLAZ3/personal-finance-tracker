from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from ..models import db, User
from ..services.plaid_service import create_link_token, exchange_public_token

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')

    if User.query.filter_by(username=username).first():
        return jsonify({'message': 'User already exists'}), 409

    new_user = User(
        username=username,
        email=email,
        password_hash=generate_password_hash(password)
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'}), 201

@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()

    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({'message': 'Invalid credentials'}), 401

    access_token = create_access_token(identity=user.id)
    return jsonify({'access_token': access_token}), 200

@auth.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    return jsonify(logged_in_as=user.username), 200

@auth.route('/create_link_token', methods=['POST'])
@jwt_required()
def create_link():
    current_user_id = get_jwt_identity()
    link_token = create_link_token(current_user_id)
    return jsonify({'link_token': link_token})

@auth.route('/exchange_public_token', methods=['POST'])
@jwt_required()
def exchange_token():
    public_token = request.json.get('public_token')
    access_token = exchange_public_token(public_token)
    if access_token:
        return jsonify({'access_token': access_token}), 200
    return jsonify({'error': 'Failed to exchange public token'}), 400
