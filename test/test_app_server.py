import unittest
from unittest.mock import patch

from app import app
from app_server import build_demo_scheduler, book_client_for_date, list_available_slots


class AppServerTests(unittest.TestCase):
    def test_demo_scheduler_contains_expected_monday_slots(self) -> None:
        scheduler = build_demo_scheduler()

        slots = list_available_slots(scheduler, "2026-09-21")
        slot_map = {slot["time"]: slot for slot in slots}

        self.assertTrue(slot_map["09:00"]["available"])
        self.assertTrue(slot_map["10:00"]["available"])
        self.assertTrue(slot_map["16:00"]["available"])
        self.assertNotIn("09:30", slot_map)
        self.assertFalse(slot_map["16:30"]["available"])
        self.assertTrue(slot_map["16:30"]["protected_booking"])

    def test_demo_scheduler_has_weekday_slots(self) -> None:
        scheduler = build_demo_scheduler()

        slots = list_available_slots(scheduler, "2026-09-22")

        self.assertTrue(slots[0]["available"])
        self.assertEqual(slots[0]["time"], "09:00")
        self.assertEqual(slots[-1]["time"], "16:00")

    def test_booking_endpoint_logic_rejects_taken_slots(self) -> None:
        scheduler = build_demo_scheduler()

        with self.assertRaises(ValueError):
            book_client_for_date(scheduler, "2026-09-21", "16:30")

    def test_booking_api_sends_confirmation_email(self) -> None:
        client = app.test_client()

        with patch("app.send_booking_confirmation", return_value=True) as send_email:
            response = client.post(
                "/api/book",
                json={
                    "name": "Alex Example",
                    "email": "alex@example.com",
                    "date": "2026-09-28",
                    "time": "09:00",
                },
            )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.get_json()["email_sent"])
        send_email.assert_called_once_with(
            "alex@example.com", "Alex Example", "2026-09-28", "09:00"
        )


if __name__ == "__main__":
    unittest.main()
