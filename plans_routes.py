from flask import Blueprint, jsonify, request
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
    plans_collection.insert_one(data)
    return jsonify({"message": "Plan saved!"}), 201
