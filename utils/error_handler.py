from flask import jsonify

def register_error_handlers(app):
    @app.errorhandler(404)
    def not_found_error(error):
        return jsonify({"error": "Not Found", "message": str(error)}), 404

    @app.errorhandler(405)
    def method_not_allowed_error(error):
        return jsonify({"error": "Method Not Allowed", "message": str(error)}), 405

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({"error": "Internal Server Error", "message": str(error)}), 500
