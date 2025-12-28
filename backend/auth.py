import random
import jwt
import datetime
import smtplib
from email.message import EmailMessage
from config import EMAIL_ADDRESS, EMAIL_PASSWORD, JWT_SECRET, JWT_EXPIRY_SECONDS
from database import users_col, otp_col


def generate_otp():
    return str(random.randint(100000, 999999))


def send_otp_email(to_email, otp):
    msg = EmailMessage()
    msg.set_content(f"Your OTP is: {otp}\nValid for 5 minutes.")
    msg["Subject"] = "Your Login OTP"
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = to_email

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(msg)


def create_jwt(email):
    payload = {
        "email": email,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=JWT_EXPIRY_SECONDS)
    }
    return jwt.encode(payload, JWT_SECRET, algorithm="HS256")
