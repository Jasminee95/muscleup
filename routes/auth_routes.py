from flask import Blueprint, jsonify, request
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_cors import cross_origin
from flask_login import login_user, logout_user, login_required, current_user
from config import get_db_connection
from models import User

auth = Blueprint("auth", __name__)

@auth.route("/register", methods=["POST"])
@cross_origin(origins="http://localhost:3000", supports_credentials=True)
def register():
    data = request.get_json()
    username = data.get("username")
    email = data.get("email", "").strip().lower()
    password = data.get("password")

    if not username or not email or not password:
        return jsonify({"error": "Missing fields"}), 400

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
    existing = cursor.fetchone()
    if existing:
        conn.close()
        return jsonify({"error": "User already exists"}), 400

    hashed_pw = generate_password_hash(password)
    cursor.execute(
        "INSERT INTO users (email, password_hash, username) VALUES (%s, %s, %s)",
        (email, hashed_pw, username),
    )
    conn.commit()
    conn.close()
    return jsonify({"message": "User registered successfully"}), 201


@auth.route("/login", methods=["POST"])
@cross_origin(origins="http://localhost:3000", supports_credentials=True)
def login():
    data = request.get_json()
    email = data.get("email", "").strip().lower()
    password = data.get("password")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
    user = cursor.fetchone()
    conn.close()

    if not user or not check_password_hash(user["password_hash"], password):
        return jsonify({"error": "Invalid email or password"}), 401

    user_obj = User(user["id"], user["email"], user["username"])
    login_user(user_obj)
    return jsonify({"message": "Login successful"}), 200


@auth.route("/logout", methods=["POST"])
@cross_origin(origins="http://localhost:3000", supports_credentials=True)
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logged out"}), 200


@auth.route("/me", methods=["GET"])
@cross_origin(origins="http://localhost:3000", supports_credentials=True)
@login_required
def get_current_user():
    if not current_user.is_authenticated:
        return jsonify({"error": "Not logged in"}), 401

    user_data = {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
    }
    return jsonify(user_data), 200