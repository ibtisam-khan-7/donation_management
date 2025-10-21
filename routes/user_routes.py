from flask import Blueprint, request
from controllers.user_controller import (
    get_all_users_controller,
    delete_user_controller,
    update_user_controller,
)
from utils.auth_middleware import token_required
from utils.role_required import role_required

user_routes = Blueprint("user_routes", __name__)

# Get all users (Admin only)
@user_routes.route("/users", methods=["GET"])
@token_required
@role_required(["admin"])
def get_all_users():
    return get_all_users_controller()


# Delete user (Admin only)
@user_routes.route("/users/<user_id>", methods=["DELETE"])
@token_required
@role_required(["admin"])
def delete_user(user_id):
    return delete_user_controller(user_id)


# Update user (Admin only)
@user_routes.route("/users/<user_id>", methods=["PUT"])
@token_required
@role_required(["admin"])
def update_user(user_id):
    data = request.get_json()
    return update_user_controller(user_id, data)
