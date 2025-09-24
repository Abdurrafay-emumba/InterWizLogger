# app.py
import os
import json
import re
from datetime import datetime, timezone, date

from flask import Flask, request, jsonify

app = Flask(__name__)
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

def safe_basename_from_email(email: str) -> str:
    """
    Keep it filesystem-safe: letters, numbers, underscore, hyphen only.
    """

    return re.sub(r"[^a-z0-9_-]", "_", email)

@app.post("/log")
def log_event():
    # Accept JSON or form data
    data = request.get_json(silent=True) or request.form.to_dict() or {}
    email = data.get("email")
    event = data.get("event") or data.get("Event")  # be a bit lenient on key casing

    if not email or not event:
        return jsonify({"ok": False, "error": "Both 'email' and 'event' are required."}), 400

    today = date.today()
    now = datetime.now()
    # Build log line
    entry = {
        "date": today.strftime("%Y-%m-%d"),
        "timestamp": now.strftime("%H:%M:%S"),
        "email": email,
        "event": event,
    }

    # Choose file by email local-part
    fname = safe_basename_from_email(email) + ".jsonl"
    fpath = os.path.join(LOG_DIR, fname)

    # Append as JSON line
    with open(fpath, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False, indent=4) + "\n")

    return jsonify({"ok": True, "saved_to": fpath})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=4598, debug=True)
