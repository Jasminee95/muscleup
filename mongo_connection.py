from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")

db = client["muscleup_schedule"]

plans_collection = db["plans"]
