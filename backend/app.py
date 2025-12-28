from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime, timedelta
import jwt

from config import SECRET_KEY, JWT_SECRET
from database import users_col, otp_col, levels_col, topics_col
from auth import generate_otp, send_otp_email, create_jwt, hash_password, verify_password
from functools import wraps

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.headers.get("Authorization")

        if not auth or not auth.startswith("Bearer "):
            return jsonify({"error": "Token required"}), 401

        token = auth.split(" ")[1]

        try:
            decoded = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        except:
            return jsonify({"error": "Invalid token"}), 401

        request.user = decoded  # store user info
        return f(*args, **kwargs)

    return decorated



app = Flask(__name__)
CORS(app)


# -------------------- AUTH --------------------

@app.route("/auth/signup", methods=["POST"])
def signup():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email and password required"}), 400

    # Check if user already exists
    if users_col.find_one({"email": email}):
        return jsonify({"error": "User already exists"}), 400

    # Hash password and store temporarily in OTP collection
    hashed_password = hash_password(password)
    
    # Generate OTP
    otp = generate_otp()
    expires_at = datetime.utcnow() + timedelta(minutes=5)

    # Store OTP with hashed password
    otp_col.delete_many({"email": email})
    otp_col.insert_one({
        "email": email,
        "password": hashed_password,
        "otp": otp,
        "expires_at": expires_at
    })

    # Send OTP email
    send_otp_email(email, otp)

    return jsonify({"message": "OTP sent to email. Please verify to complete signup."})


@app.route("/auth/send-otp", methods=["POST"])
def send_otp():
    data = request.json
    email = data.get("email")

    if not email:
        return jsonify({"error": "Email required"}), 400

    otp = generate_otp()
    expires_at = datetime.utcnow() + timedelta(minutes=5)

    otp_col.update_one(
        {"email": email},
        {
            "$set": {
                "otp": otp,
                "expires_at": expires_at
            }
        },
        upsert=True
    )

    send_otp_email(email, otp)

    return jsonify({"message": "OTP sent successfully"})


@app.route("/auth/verify-otp", methods=["POST"])
def verify_otp():
    data = request.json
    email = data.get("email")
    otp = data.get("otp")

    record = otp_col.find_one({"email": email})

    if not record:
        return jsonify({"error": "OTP not found"}), 400

    if record["otp"] != otp:
        return jsonify({"error": "Invalid OTP"}), 400

    if datetime.utcnow() > record["expires_at"]:
        return jsonify({"error": "OTP expired"}), 400

    # ✅ INSERT HERE (this is the exact place)
    if not users_col.find_one({"email": email}):
        users_col.insert_one({
            "email": email,
            "password": record["password"],
            "is_verified": True,
            "created_at": datetime.utcnow()
        })

    otp_col.delete_one({"email": email})

    return jsonify({"message": "Account verified successfully"})


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
@token_required
def profile():
    email = request.user["email"]

    user = users_col.find_one(
        {"email": email},
        {"_id": 0, "password": 0}
    )

    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify(user)


@app.route("/auth/login", methods=["POST"])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    user = users_col.find_one({"email": email})

    if not user:
        return jsonify({"error": "User not found"}), 404

    if not user.get("is_verified"):
        return jsonify({"error": "Email not verified"}), 403

    if not verify_password(password, user["password"]):
        return jsonify({"error": "Invalid password"}), 401

    token = create_jwt(email)

    return jsonify({
        "message": "Login successful",
        "token": token
    })




# --------------------

if __name__ == "__main__":
    app.run(debug=True)
