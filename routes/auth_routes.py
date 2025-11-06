from flask import Blueprint, request, jsonify
from flask_bcrypt import generate_password_hash, check_password_hash
from config import get_db_connection
from flask_login import login_user, login_required, logout_user, current_user
from models import User
from routes.plans_routes import plans_bp

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({'error': 'Missing fields'}), 400

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    existing_user = cursor.fetchone()

    if existing_user:
        conn.close()
        return jsonify({'error': 'User already exists'}), 400

    hashed_pw = generate_password_hash(password).decode('utf-8')
    cursor.execute(
        "INSERT INTO users (email, password_hash, username) VALUES (%s, %s, %s)",
        (email, hashed_pw, username)
    )
    conn.commit()
    conn.close()

    return jsonify({'message': 'User registered successfully'}), 201


@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    user = cursor.fetchone()
    conn.close()

    if not user or not check_password_hash(user['password_hash'], password):
        return jsonify({'error': 'Invalid email or password'}), 401

    logged_in_user = User(user['id'], user['email'], user['username'])
    login_user(logged_in_user)

    return jsonify({
        'message': 'Login successful',
        'user': {'id': user['id'], 'email': user['email'], 'username': user['username']}
    }), 200

@auth.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logged out successfully'}), 200

@auth.route('/profile', methods=['GET'])
@login_required
def profile():
    return jsonify({
        "id": current_user.id,
        "email": current_user.email,
        "username": current_user.username
    })