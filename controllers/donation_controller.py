from flask import jsonify
from models.donation_model import donations_collection
from datetime import datetime
from bson import ObjectId


#  Add donation
def add_donation_controller(data):
    try:
        if not all(key in data for key in ("donor_name", "amount")):
            return jsonify({"error": "Missing required fields: donor_name, amount"}), 400

        donation_data = {
            "donor_name": data["donor_name"],
            "amount": data["amount"],
            "date": data.get("date", datetime.now().strftime("%Y-%m-%d")),
        }

        donations_collection.insert_one(donation_data)
        return jsonify({"message": "Donation added successfully!"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


#  Get all donations
def get_all_donation_controller():
    donations = list(donations_collection.find({}))
    for donation in donations:
        donation["_id"] = str(donation["_id"])  # Convert ObjectId to string
    return jsonify(donations), 200


#  Update donation
def update_donation_controller(donation_id, data):
    try:
        result = donations_collection.update_one(
            {"_id": ObjectId(donation_id)}, {"$set": data}
        )
        if result.matched_count == 0:
            return jsonify({"error": "Donation not found"}), 404
        return jsonify({"message": "Donation updated successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


#  Delete donation
def delete_donation_controller(donation_id):
    try:
        result = donations_collection.delete_one({"_id": ObjectId(donation_id)})
        if result.deleted_count == 0:
            return jsonify({"error": "Donation not found"}), 404
        return jsonify({"message": "Donation deleted successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
