# auth_routes.py
from flask import Blueprint, request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from db import db
from models import User

# Create a Blueprint for authentication
auth_bp = Blueprint('auth', __name__)

# Register route
@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    # Extract required fields
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    role = data.get('role')

    # Validate required fields
    if not username or not email or not password or not role:
        return jsonify({'error': 'All fields are required: username, email, password, and role.'}), 400

    # Ensure role is either 'user' or 'organizer'
    if role not in ['user', 'organizer']:
        return jsonify({'error': "Role must be either 'user' or 'organizer'."}), 400

    # Check if email or username already exists
    existing_user = User.query.filter((User.email == email) | (User.username == username)).first()
    if existing_user:
        return jsonify({'error': 'Username or email already exists.'}), 409

    # Hash the password and create the user
    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
    new_user = User(username=username, email=email, password=hashed_password, role=role)

    try:
        db.session.add(new_user)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'An error occurred while creating the user.'}), 500

    # Return user details in the response
    return jsonify({
        'message': 'User registered successfully!',
        'user': {
            'username': new_user.username,
            'email': new_user.email,
            'role': new_user.role
        }
    }), 201

# Login route
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    # Find user by email
    user = User.query.filter_by(email=email).first()
    
    if not user or not check_password_hash(user.password, password):
        return jsonify({"message": "Invalid credentials"}), 401

    # Generate a JWT token for the user
    token = create_access_token(identity=user.id)

    # Return user data and the token in the response
    return jsonify({
        "message": "Login successful",
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": user.role
        },
        "token": token
    }), 200

# Route for checking if the user is logged in
@auth_bp.route('/check_login', methods=['GET'])
def check_login():
    if 'user_id' in session:
        return jsonify({"message": "User is logged in", "username": session['username']}), 200
    else:
        return jsonify({"message": "User is not logged in"}), 401
    
# Home route
@auth_bp.route('/')
def home():
    if 'user_id' in session:
        return jsonify({"message": f"Welcome {session['username']}"}), 200
    else:
        return jsonify({"message": "You are not logged in"}), 401

# Logout route
@auth_bp.route('/logout', methods=['GET'])
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    session.pop('role', None)
    return redirect(url_for('home'))