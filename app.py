from __future__ import annotations

import smtplib

from flask import Flask, jsonify, request, send_file

from app_server import build_demo_scheduler, list_available_slots, book_client_for_date
from email_service import send_booking_confirmation

app = Flask(__name__, static_folder=".", static_url_path="")
app.config["JSON_SORT_KEYS"] = False

scheduler = build_demo_scheduler()


@app.route("/")
def index():
    return send_file("index.html")


@app.route("/api/slots")
def api_slots():
    date = request.args.get("date")
    if not date:
        return jsonify({"error": "date parameter is required"}), 400

    try:
        slots = list_available_slots(scheduler, date)
        return jsonify(slots)
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400


@app.route("/api/book", methods=["POST"])
def api_book():
    payload = request.get_json(silent=True) or {}
    name = str(payload.get("name", "")).strip()
    email = str(payload.get("email", "")).strip()
    date = payload.get("date")
    time = payload.get("time")

    if not date or not time or not name or not email:
        return jsonify({"message": "name, email, date, and time are required"}), 400

    try:
        bookings = book_client_for_date(scheduler, date, time)
    except ValueError as exc:
        return jsonify({"message": str(exc)}), 400

    email_sent = False
    try:
        email_sent = send_booking_confirmation(email, name, date, time)
    except (OSError, smtplib.SMTPException, ValueError):
        app.logger.exception("Unable to send booking confirmation email")

    return jsonify(
        {
            "message": "Booking confirmed",
            "bookings": bookings,
            "email_sent": email_sent,
        }
    ), 200


if __name__ == "__main__":
    app.run(debug=True)
