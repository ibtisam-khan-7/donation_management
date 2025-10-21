from flask import Blueprint, jsonify, request
from bson import ObjectId
from utils.auth_middleware import token_required, admin_required
from models.donation_model import donations_collection
from utils.role_required import role_required
from controllers.donation_controller import (
    add_donation_controller,
    get_all_donation_controller,
    update_donation_controller,
    delete_donation_controller,
)
donation_routes = Blueprint("donation_routes", __name__)


@donation_routes.route("/add_donation", methods=["POST"])
@token_required
@role_required(["donor", "admin"])
def add_donation():
    data = request.get_json()
    return add_donation_controller(data)


@donation_routes.route("/donations", methods=["GET"])
@token_required
@role_required(["admin", "volunteer", "donor"])
def get_donations():
    return get_all_donation_controller()


@donation_routes.route("/update_donation/<donation_id>", methods=["PUT"])
@admin_required
@role_required(["admin", "donor"])
def update_donation(donation_id):
    data = request.get_json()
    user = request.user

    donation = donations_collection.find_one({"_id": ObjectId(donation_id)})

    if not donation:
        return jsonify({"error": "Donation not found"}), 404

    if user["role"] == "donor" and donation["user_id"] != user["id"]:
        return jsonify({"error": "You can only edit your own donation!"}), 403

    donations_collection.update_one({"_id": ObjectId(donation_id)}, {"$set": data})
    return jsonify({"message": "Donation updated successfully!"}), 200


@donation_routes.route("/delete_donation/<donation_id>", methods=["DELETE"])
@token_required
@role_required(["admin", "donor"])
def delete_donation(donation_id):
    user = request.user
    donation = donations_collection.find_one({"_id": ObjectId(donation_id)})

    if not donation:
        return jsonify({"error": "Donation not found"}), 404

    
    if user["role"] == "donor" and donation["user_id"] != user["id"]:
        return jsonify({"error": "You can only delete your own donation!"}), 403

    donations_collection.delete_one({"_id": ObjectId(donation_id)})
    return jsonify({"message": "Donation deleted successfully!"}), 200

