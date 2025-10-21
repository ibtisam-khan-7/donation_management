from flask import Flask
from pymongo import MongoClient
from dotenv import load_dotenv
from routes.donation_routes import donation_routes
from utils.error_handler import register_error_handlers
from routes.auth_routes import auth_routes
from routes.user_routes import user_routes
import os

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Set Flask secret key
app.secret_key = os.getenv("FLASK_SECRET_KEY")

# Connect to MongoDB using .env variable
mongo_uri = os.getenv("MONGO_URI")
client = MongoClient(mongo_uri)
db = client["donation_management"]
donations_collection = db["donations"]


# Register routes
app.register_blueprint(donation_routes)
app.register_blueprint(auth_routes)
app.register_blueprint(user_routes, url_prefix="/api")
# Register error handlers
register_error_handlers(app)



if __name__ == "__main__":
    app.run(debug=True)
