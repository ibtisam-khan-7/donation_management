from flask import jsonify, request
from models.user_model import user_collection
from bson import ObjectId

# Get all users (Admin only)
def get_all_users_controller():
    try:
        users = []
        for user in user_collection.find({}, {"password": 0}):  # hide password
            user["_id"] = str(user["_id"])
            users.append(user)
        return jsonify(users), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Delete a user (Admin only)
def delete_user_controller(user_id):
    try:
        result = user_collection.delete_one({"_id": ObjectId(user_id)})
        if result.deleted_count == 0:
            return jsonify({"error": "User not found"}), 404
        return jsonify({"message": "User deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Update user role or name (Admin only)
def update_user_controller(user_id, data):
    try:
        update_fields = {}
        if "name" in data:
            update_fields["name"] = data["name"]
        if "role" in data:
            update_fields["role"] = data["role"]

        if not update_fields:
            return jsonify({"error": "No valid fields to update"}), 400

        result = user_collection.update_one(
            {"_id": ObjectId(user_id)}, {"$set": update_fields}
        )
        if result.matched_count == 0:
            return jsonify({"error": "User not found"}), 404

        return jsonify({"message": "User updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
