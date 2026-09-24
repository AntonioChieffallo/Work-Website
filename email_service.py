from __future__ import annotations

import os
import smtplib
from email.message import EmailMessage


def send_booking_confirmation(
    recipient: str,
    client_name: str,
    date: str,
    time: str,
) -> bool:
    """Send a confirmation email when SMTP settings are configured."""
    host = os.getenv("SMTP_HOST")
    if not host:
        return False

    port = int(os.getenv("SMTP_PORT", "587"))
    username = os.getenv("SMTP_USERNAME")
    password = os.getenv("SMTP_PASSWORD")
    sender = os.getenv("SMTP_FROM", username or "noreply@localhost")

    message = EmailMessage()
    message["Subject"] = "Your appointment is confirmed"
    message["From"] = sender
    message["To"] = recipient
    message.set_content(
        f"Hi {client_name},\n\n"
        f"Your appointment is confirmed for {date} at {time}.\n\n"
        "Thank you."
    )

    with smtplib.SMTP(host, port, timeout=10) as server:
        if os.getenv("SMTP_USE_TLS", "true").lower() == "true":
            server.starttls()
        if username and password:
            server.login(username, password)
        server.send_message(message)

    return True
