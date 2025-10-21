from flask import jsonify, request

def role_required(allowed_roles):
    def decorator(f):
        def wrapper(*args, **kwargs):
            user = getattr(request, "user", None)
            if not user:
                return jsonify({"error": "Token missing or invalid!"}), 401

            user_role = user.get("role", ""). lower()
            if user_role not in allowed_roles:
                return jsonify({"error": "Access denied!"}), 403

            return f(*args, **kwargs)
        wrapper.__name__ = f.__name__
        return wrapper
    return decorator