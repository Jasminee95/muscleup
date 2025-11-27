from flask import Blueprint, jsonify, request
import requests

exercises_bp = Blueprint("exercises_bp", __name__)

BASE_URL = "https://exercisedb-api.vercel.app/api/v1/exercises"


@exercises_bp.route("/exercises", methods=["GET"])
def get_exercises():
    search = request.args.get("search", "").strip().lower()

    if not search:
        return jsonify({"data": [], "success": True}), 200

    try:
        url = f"{BASE_URL}?search={search}"
        response = requests.get(url)
        raw = response.json()

        exercises = raw.get("data", [])

        mapped = []
        for ex in exercises:
            mapped.append({
                "exerciseId": ex.get("exerciseId"),
                "name": ex.get("name"),
                "bodyPart": (ex.get("bodyParts") or [None])[0],
                "target": (ex.get("targetMuscles") or [None])[0],
                "equipment": (ex.get("equipments") or [None])[0],
                "imageUrl": ex.get("gifUrl"),
            })

        return jsonify({"data": mapped, "success": True}), 200

    except Exception as e:
        print("API error:", e)
        return jsonify({"success": False, "error": str(e)}), 500
