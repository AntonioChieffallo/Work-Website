import unittest

from main import build_demo_output


class MainDemoTests(unittest.TestCase):
    def test_demo_output_shows_protected_booking_after_schedule_change(self) -> None:
        output = build_demo_output()

        self.assertIn("Calendar Scheduler Demo", output)
        self.assertIn("Protected bookings after schedule change: 1", output)
        self.assertIn("Protected time: 16:30", output)


if __name__ == "__main__":
    unittest.main()
