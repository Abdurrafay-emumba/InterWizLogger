from datetime import datetime, date

from flask import Flask, request, jsonify

from google_spread_sheet_queue import google_sheets_queue

app = Flask(__name__)

sheets_queue = google_sheets_queue("InterWiz App Logs")
sheets_queue.start_worker()

@app.post("/log")
def log_event():
    try:
        # Accept JSON or form data
        data = request.get_json(silent=True) or request.form.to_dict() or {}
        email = data.get("email")
        event = data.get("event") or data.get("Event")  # be a bit lenient on key casing

        if not email or not event:
            return jsonify({"ok": False, "error": "Both 'email' and 'event' are required."}), 400

        today = date.today()
        now = datetime.now()

        csv_data = [
                        ["Date", "Time", "Email", "Event"],
                        [today.strftime("%Y-%m-%d"), now.strftime("%H:%M:%S"), email, event]
                    ]

        sheets_queue.enqueue(csv_data)

        return jsonify({"ok": True, "saved_to": "Google Sheets"})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=4598, debug=True), 500
