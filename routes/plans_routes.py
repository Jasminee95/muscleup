from flask import Blueprint, jsonify, request
from flask_jwt_extended import current_user
from flask_login import login_required
from mongo_connection import plans_collection

plans_bp = Blueprint("plans", __name__)

@plans_bp.route("/plans", methods=["GET"])
@login_required
def get_plans():
    plans = list(plans_collection.find({}, {"_id": 0}))
    return jsonify(plans)

@plans_bp.route("/plans", methods=["POST"])
@login_required
def create_plan():
    data = request.get_json()
    plan = {
        "user_id": current_user.id,
        "title": data.get("title"),
        "description": data.get("description"),
        "days": data.get("days"),
    }
    plans_collection.insert_one(plan)
    return jsonify({"message": "Plan saved!"}), 201

@plans_bp.route("/plans", methods=["GET"])
@login_required
def get_plan():
    user_plans = list(plans_collection.find({"user_id": current_user.id}))
    for plan in user_plans:
        plan["_id"] = str(plan["_id"])
        return jsonify(user_plans)