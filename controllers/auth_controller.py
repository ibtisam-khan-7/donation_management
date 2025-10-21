from flask import jsonify, request
from models.user_model import user_collection
from bson import ObjectId
from dotenv import load_dotenv
import bcrypt
import jwt
import os
import datetime

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY", "defaultsecret")

# user registration
def registration_user_controller(data):
    try:

        if not all(k in data for k in ("name", "email", "password", "role")):
            return jsonify({"error": "All fields (name, email, password, role) required"}), 400
    
        if user_collection.find_one({"email": data["email"]}):
            return jsonify({"error": "Email already registered"}), 400
        
        hashed_pw = bcrypt.hashpw(data["password"].encode('utf-8'), bcrypt.gensalt())
        user_data = {
            "name": data["name"],
            "email": data["email"],
            "password": hashed_pw.decode("utf-8"),
            "role": data["role"],
            "created_at": datetime.datetime.now()
        }

        user_collection.insert_one(user_data)
        return jsonify({"message": "User registered successfully!"}), 201
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
# user login

def login_user_controller(data):
    try:
        if not all(k in data for k in ("email", "password")):
            return jsonify({"error": "Email and password required"}), 400

        user = user_collection.find_one({"email": data["email"]})
        if not user:
            return jsonify({"error": "Invalid email or password"}), 401

        if not bcrypt.checkpw(data["password"].encode('utf-8'), user["password"].encode('utf-8')):
            return jsonify({"error": "Invalid email or password"}), 401
        
        payload = {
            "email": user["email"],
            "role": user["role"],
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=2)
        }

        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
        return jsonify({"token": token}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500