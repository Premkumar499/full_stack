from pymongo import MongoClient
from config import MONGO_URI

client = MongoClient(MONGO_URI)
db = client["prompt_library"]

users_col = db["users"]
otp_col = db["otp"]
levels_col = db["levels"]
topics_col = db["topics"]
