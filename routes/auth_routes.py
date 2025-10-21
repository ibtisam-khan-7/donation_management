from flask import Blueprint, request
from controllers.auth_controller import registration_user_controller, login_user_controller

auth_routes = Blueprint("auth_routes", __name__)

@auth_routes.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    return registration_user_controller(data)

@auth_routes.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    return login_user_controller(data)