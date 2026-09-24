# Work-Website

A lightweight Python calendar scheduling framework for business owners and clients.

## Features implemented
- Recurring weekly working hours (for example, Monday-Friday 09:00-17:00)
- Per-date custom schedule overrides (including marking specific dates closed)
- Client booking on available time slots
- Retrospective schedule updates that still preserve existing client bookings

## Run demo
```bash
python "C:\Users\achie\SomeCodingShit\Work-Website\app.py"
```

## Configure confirmation email
Set these environment variables before starting the Flask app:

```text
SMTP_HOST=smtp.example.com
SMTP_PORT=587
SMTP_USERNAME=your-account@example.com
SMTP_PASSWORD=your-password
SMTP_FROM=your-account@example.com
SMTP_USE_TLS=true
```

Bookings still work without SMTP settings, but no confirmation email is sent.

## Run tests
```bash
python -m unittest discover -s test -p 'test_*.py'
```
