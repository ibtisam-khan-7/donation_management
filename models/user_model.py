from pymongo import MongoClient
from models.donation_model import db

client = MongoClient("mongodb://localhost:27017/")
db = client['donation_management']
user_collection = db['users']