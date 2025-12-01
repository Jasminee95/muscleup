from flask import Blueprint, jsonify, request
from flask_login import current_user, login_required
from mongo_connection import plans_collection

plans_bp = Blueprint("plans", __name__)

@plans_bp.route("/plans", methods=["POST"])
@login_required
def add_to_plan():
    data = request.get_json()

    day = list(data["days"].keys())[0]
    exercise = data["days"][day][0]

    plans_collection.update_one(
        {"user_id": current_user.id, "day": day},
        {"$push": {"exercises": exercise}},
        upsert=True
    )

    return jsonify({"message": "Exercise added to plan!"}), 201


@plans_bp.route("/plans", methods=["GET"])
@login_required
def get_plan():
    user_plans = list(plans_collection.find({"user_id": current_user.id}))
    for plan in user_plans:
        plan["_id"] = str(plan["_id"])
    return jsonify(user_plans)


@plans_bp.route("/plans/remove", methods=["POST", "OPTIONS"])
@login_required
def remove_from_plan():
    if request.method == "OPTIONS":
        return jsonify({"status": "ok"}), 200

    data = request.get_json()
    day = data.get("day")
    exercise = data.get("exercise")

    if not day or not exercise:
        return jsonify({"error": "Missing day or exercise"}), 400

    result = plans_collection.update_one(
        {"user_id": current_user.id, "day": day},
        {"$pull": {"exercises": exercise}}
    )

    if result.modified_count == 0:
        return jsonify({"error": "Exercise not found in plan"}), 404

    return jsonify({"message": "Exercise removed from plan"}), 200