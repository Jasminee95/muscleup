from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from config import get_db_connection

favorites_bp = Blueprint("favorites_bp", __name__)

@favorites_bp.route('/favorites', methods=['GET'])
@login_required
def get_favorites():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM favorites WHERE user_id = %s", (current_user.id,))
    favorites = cursor.fetchall()
    conn.close()
    return jsonify(favorites), 200

@favorites_bp.route('/favorites', methods=['POST'])
@login_required
def add_favorites():
    data = request.get_json()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO favorites (user_id, exercise_id, exercise_name, body_part, target, equipment, gif_url)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """,(
        current_user.id,
        data.get("exercise_id"),
        data.get("exercise_name"),
        data.get("body_part"),
        data.get("target"),
        data.get("equipment"),
        data.get("gif_url")
    ))
    conn.commit()
    conn.close()
    return jsonify({"message": "Favorite added!"}), 201

@favorites_bp.route('/<exercise_id>', methods=['DELETE'])
@login_required
def delete_favorite(exercise_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM favorites WHERE user_id = %s AND exercise_id = %s",
                   (current_user.id, exercise_id))
    conn.commit()
    conn.close()
    return jsonify({"message": "Favorite removed!"}), 200