from flask import Blueprint, jsonify, request
from bson import ObjectId
from bson.errors import InvalidId
from utils.auth_middleware import token_required, admin_required, role_required
from models.donation_model import donations_collection
from controllers.donation_controller import (
    add_donation_controller,
    get_all_donation_controller,
)

# Blueprint initialization
donation_routes = Blueprint("donation_routes", __name__)


# -----------------------------
# Add Donation (Admin / Donor)
# -----------------------------
@donation_routes.route("/add_donation", methods=["POST"])
@token_required
@role_required(["donor", "admin"])
def add_donation():
    data = request.get_json()
    user = request.user

    if not data:
        return jsonify({"error": "Missing donation data"}), 400

    return add_donation_controller(data, user)


# -----------------------------
# View Donations (Admin / Volunteer / Donor)
# -----------------------------
@donation_routes.route("/donations", methods=["GET"])
@token_required
@role_required(["admin", "volunteer", "donor"])
def get_donations():
    return get_all_donation_controller()


# -----------------------------
# Update Donation (Admin or Owner Donor)
# -----------------------------
@donation_routes.route("/update_donation/<donation_id>", methods=["PUT"])
@token_required
@role_required(["admin", "donor"])
def update_donation(donation_id):
    user = request.user
    data = request.get_json()

    try:
        donation = donations_collection.find_one({"_id": ObjectId(donation_id)})
    except InvalidId:
        return jsonify({"error": "Invalid donation ID"}), 400

    if not donation:
        return jsonify({"error": "Donation not found"}), 404

    # Donor can only update their own donation
    if user["role"] == "donor" and str(donation["user_id"]) != str(user["id"]):
        return jsonify({"error": "You can only edit your own donation!"}), 403

    donations_collection.update_one({"_id": ObjectId(donation_id)}, {"$set": data})
    return jsonify({"message": "Donation updated successfully!"}), 200


# -----------------------------
# Delete Donation (Admin or Owner Donor)
# -----------------------------
@donation_routes.route("/delete_donation/<donation_id>", methods=["DELETE"])
@token_required
@role_required(["admin", "donor"])
def delete_donation(donation_id):
    user = request.user

    try:
        donation = donations_collection.find_one({"_id": ObjectId(donation_id)})
    except InvalidId:
        return jsonify({"error": "Invalid donation ID"}), 400

    if not donation:
        return jsonify({"error": "Donation not found"}), 404

    # Donor can only delete their own donation
    if user["role"] == "donor" and str(donation["user_id"]) != str(user["id"]):
        return jsonify({"error": "You can only delete your own donation!"}), 403

    donations_collection.delete_one({"_id": ObjectId(donation_id)})
    return jsonify({"message": "Donation deleted successfully!"}), 200
