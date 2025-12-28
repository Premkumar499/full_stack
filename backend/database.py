from pymongo import MongoClient
from config import MONGO_URI
import certifi

client = MongoClient(
    MONGO_URI,
    tlsCAFile=certifi.where(),
    serverSelectionTimeoutMS=5000,
    connectTimeoutMS=5000,
    socketTimeoutMS=5000
)
db = client["prompt_library"]

users_col = db["users"]
otp_col = db["otp"]
levels_col = db["levels"]
topics_col = db["topics"]
