import unittest

from app_server import build_demo_scheduler, book_client_for_date, list_available_slots


class AppServerTests(unittest.TestCase):
    def test_demo_scheduler_contains_expected_monday_slots(self) -> None:
        scheduler = build_demo_scheduler()

        slots = list_available_slots(scheduler, "2026-09-21")
        slot_map = {slot["time"]: slot for slot in slots}

        self.assertTrue(slot_map["09:00"]["available"])
        self.assertFalse(slot_map["16:30"]["available"])
        self.assertTrue(slot_map["16:30"]["protected_booking"])

    def test_booking_endpoint_logic_rejects_taken_slots(self) -> None:
        scheduler = build_demo_scheduler()

        with self.assertRaises(ValueError):
            book_client_for_date(scheduler, "2026-09-21", "16:30")


if __name__ == "__main__":
    unittest.main()
