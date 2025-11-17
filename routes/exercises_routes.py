from flask import Blueprint, jsonify, request
import requests
import os

exercises_bp = Blueprint("exercises_bp", __name__)

@exercises_bp.route("/exercises", methods=["GET"])
def get_exercises():
    search = request.args.get("search", "").lower()

    if not search:
        return jsonify({"data": [], "success": True}), 200

    url = f"https://exercisedb-api1.p.rapidapi.com/api/v1/exercises/name={search}"

    headers = {
        "x-rapidapi-key": os.getenv("EXERCISE_API_KEY"),
        "x-rapidapi-host": "exercisedb-api1.p.rapidapi.com"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        exercises = response.json()

        return jsonify({
            "data": exercises,
            "success": True
        }), 200

    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500