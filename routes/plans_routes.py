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