import unittest

from calendar_scheduler import CalendarScheduler


class CalendarSchedulerTests(unittest.TestCase):
    def test_uses_recurring_weekly_hours_to_create_available_slots(self) -> None:
        scheduler = CalendarScheduler()
        scheduler.set_recurring_hours(0, "09:00", "10:00")  # Monday

        slots = scheduler.list_slots("2026-09-21")  # Monday

        self.assertEqual(
            slots,
            [
                {"time": "09:00", "available": True, "protected_booking": False},
                {"time": "09:30", "available": True, "protected_booking": False},
            ],
        )

    def test_date_specific_override_takes_priority_over_recurring_schedule(self) -> None:
        scheduler = CalendarScheduler()
        scheduler.set_recurring_hours(0, "09:00", "17:00")
        scheduler.set_date_hours("2026-09-21", "13:00", "14:00")

        slots = scheduler.list_slots("2026-09-21")

        self.assertEqual(
            slots,
            [
                {"time": "13:00", "available": True, "protected_booking": False},
                {"time": "13:30", "available": True, "protected_booking": False},
            ],
        )

    def test_clients_can_only_book_currently_available_slots(self) -> None:
        scheduler = CalendarScheduler()
        scheduler.set_recurring_hours(0, "09:00", "10:00")

        scheduler.book_client("2026-09-21", "09:30")

        slots = scheduler.list_slots("2026-09-21")

        selected = [slot for slot in slots if slot["time"] == "09:30"][0]
        self.assertFalse(selected["available"])

        with self.assertRaisesRegex(ValueError, "not available"):
            scheduler.book_client("2026-09-21", "09:30")

    def test_retrospective_schedule_changes_preserve_existing_client_bookings(self) -> None:
        scheduler = CalendarScheduler()
        scheduler.set_recurring_hours(0, "09:00", "17:00")
        scheduler.book_client("2026-09-21", "16:30")

        scheduler.set_recurring_hours(0, "09:00", "12:00")

        slots = scheduler.list_slots("2026-09-21")

        protected_slot = [slot for slot in slots if slot["time"] == "16:30"][0]
        self.assertEqual(
            protected_slot,
            {"time": "16:30", "available": False, "protected_booking": True},
        )
        self.assertEqual(scheduler.get_bookings("2026-09-21"), ["16:30"])


if __name__ == "__main__":
    unittest.main()
