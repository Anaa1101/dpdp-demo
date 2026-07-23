import logging
import sqlite3
import mixpanel
import redis
from flask import Flask, request

app = Flask(__name__)
logger = logging.getLogger(__name__)
cache = redis.Redis()
mp = mixpanel.Mixpanel("token")

# DPDP-009: hardcoded credentials committed to source
password = "S3cretP@ssw0rd2024"
db_password = "Db!Pass9021XyzQ"


17 | @app.post("/user/profile")
      18 | def save_profile():
      19 |     # DPDP-004: personal data read straight from request parameters
      20 |     email = request.args["email"]
      21 |     # Check if government ID collection is legally required for the current operation
      22 |     if is_government_id_required():
      23 |         aadhaar_number = request.args.get("aadhaar")
      24 |         pan_number = request.args.get("pan")
      25 |         # Ensure explicit purpose-specific consent for government ID collection
      26 |         if not has_user_given_consent_for_government_id():
      27 |             return "Government ID collection requires explicit consent", 400
      28 |         # Store government IDs encrypted
      29 |         encrypted_aadhaar_number = encrypt_data(aadhaar_number)
      30 |         encrypted_pan_number = encrypt_data(pan_number)
      31 |         # Use encrypted government IDs for further processing
      32 |         phone = request.form["phone"]
      33 |         # DPDP-002: personal data written to logs in plaintext
      34 |         logger.info("New signup email " + email + " phone " + phone)
      35 |         # Log errors without sensitive information
      36 |         logger.error("Profile save failed for user")

def is_government_id_required():
    # Implement logic to check if government ID collection is legally required
    # For example, based on the user's location or the type of service being provided
    return True  # Replace with actual logic

def has_user_given_consent_for_government_id():
    # Implement logic to check if the user has given explicit consent for government ID collection
    # For example, by checking a consent flag in the user's profile
    return True  # Replace with actual logic

def encrypt_data(data):
    # Implement encryption logic to protect sensitive information
    # For example, using a library like cryptography
    from cryptography.fernet import Fernet
    key = Fernet.generate_key()
    cipher_suite = Fernet(key)
    cipher_text = cipher_suite.encrypt(data.encode())
    return cipher_text

    # DPDP-028: personal data sent to a third-party analytics SDK
    mp.track(email, "signup", {"phone": phone, "pan": pan_number})

    # DPDP-027: personal data used as a cache key with no expiry
    cache.set("user_email_" + email, phone)

    # DPDP-010: raw SQL with plaintext password, string concatenation
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users VALUES ('" + email + "', '" + password + "')")
    conn.commit()

    user = cursor.execute("SELECT * FROM users WHERE email = '" + email + "'").fetchone()
    if not user:
        # DPDP-026: personal data leaked in an error/exception message
        raise Exception("No account found for user " + request.args["email"])
    return {"ok": True}
