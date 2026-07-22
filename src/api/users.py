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


@app.post("/user/profile")
def save_profile():
    # DPDP-004: personal data read straight from request parameters
    email = request.args["email"]
    aadhaar_number = request.args["aadhaar"]
    pan_number = request.args["pan"]
    phone = request.form["phone"]

    # DPDP-002: personal data written to logs in plaintext
    logger.info("New signup email " + email + " phone " + phone)
    logger.error("Profile save failed for user aadhaar " + aadhaar_number)

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
