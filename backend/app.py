from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime, timedelta
import jwt

from config import SECRET_KEY, JWT_SECRET
from database import users_col, otp_col, levels_col, topics_col
from auth import generate_otp, send_otp_email, create_jwt

app = Flask(__name__)
CORS(app)


# -------------------- AUTH --------------------

@app.route("/auth/send-otp", methods=["POST"])
def send_otp():
    data = request.json
    email = data.get("email")

    if not email:
        return jsonify({"error": "Email required"}), 400

    otp = generate_otp()
    expires_at = datetime.utcnow() + timedelta(minutes=5)

    otp_col.delete_many({"email": email})
    otp_col.insert_one({
        "email": email,
        "otp": otp,
        "expires_at": expires_at
    })

    send_otp_email(email, otp)

    return jsonify({"message": "OTP sent successfully"})


@app.route("/auth/verify-otp", methods=["POST"])
def verify_otp():
    data = request.json
    email = data.get("email")
    otp = data.get("otp")

    if not email or not otp:
        return jsonify({"error": "Email and OTP required"}), 400

    record = otp_col.find_one({"email": email})

    if not record:
        return jsonify({"error": "OTP not found"}), 400

    if record["otp"] != otp:
        return jsonify({"error": "Invalid OTP"}), 400

    if datetime.utcnow() > record["expires_at"]:
        return jsonify({"error": "OTP expired"}), 400

    # OTP is valid → delete it
    otp_col.delete_one({"email": email})

    token = create_jwt(email)

    return jsonify({
        "message": "OTP verified successfully",
        "token": token
    })


# -------------------- CONTENT APIs --------------------

@app.route("/levels", methods=["GET"])
def get_levels():
    levels = list(levels_col.find({}, {"_id": 0}))
    return jsonify(levels)


@app.route("/topics/<int:level>", methods=["GET"])
def get_topics(level):
    topics = list(topics_col.find({"level": level}, {"_id": 0}))
    return jsonify(topics)


@app.route("/topic", methods=["POST"])
def add_topic():
    data = request.json
    topics_col.insert_one(data)
    return jsonify({"message": "Topic added"})


# -------------------- PROTECTED ROUTE EXAMPLE --------------------

def verify_token(token):
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
    except:
        return None


@app.route("/profile", methods=["GET"])
def profile():
    auth = request.headers.get("Authorization")
    if not auth:
        return jsonify({"error": "Token required"}), 401

    token = auth.split(" ")[1]
    decoded = verify_token(token)

    if not decoded:
        return jsonify({"error": "Invalid token"}), 401

    user = users_col.find_one({"email": decoded["email"]}, {"_id": 0})
    return jsonify(user)


# --------------------

if __name__ == "__main__":
    app.run(debug=True)
