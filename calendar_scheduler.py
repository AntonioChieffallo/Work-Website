from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Optional, Set


@dataclass(frozen=True)
class WorkingHours:
    start_time: str
    end_time: str


class CalendarScheduler:
    def __init__(self) -> None:
        self.weekly_hours: Dict[int, WorkingHours] = {}
        self.date_overrides: Dict[str, Optional[WorkingHours]] = {}
        self.bookings: Dict[str, Set[str]] = {}

    def set_recurring_hours(self, day_of_week: int, start_time: str, end_time: str) -> None:
        self._validate_day(day_of_week)
        self._validate_range(start_time, end_time)
        self.weekly_hours[day_of_week] = WorkingHours(start_time=start_time, end_time=end_time)

    def clear_recurring_hours(self, day_of_week: int) -> None:
        self._validate_day(day_of_week)
        self.weekly_hours.pop(day_of_week, None)

    def set_date_hours(self, date: str, start_time: str, end_time: str) -> None:
        self._validate_date(date)
        self._validate_range(start_time, end_time)
        self.date_overrides[date] = WorkingHours(start_time=start_time, end_time=end_time)

    def set_date_closed(self, date: str) -> None:
        self._validate_date(date)
        self.date_overrides[date] = None

    def clear_date_override(self, date: str) -> None:
        self._validate_date(date)
        self.date_overrides.pop(date, None)

    def get_working_hours(self, date: str) -> Optional[WorkingHours]:
        self._validate_date(date)

        if date in self.date_overrides:
            return self.date_overrides[date]

        day_of_week = self._get_day_of_week(date)
        return self.weekly_hours.get(day_of_week)

    def list_slots(self, date: str, slot_minutes: int = 30) -> List[dict]:
        self._validate_date(date)
        self._validate_slot_minutes(slot_minutes)

        working_hours = self.get_working_hours(date)
        scheduled_times: Set[str] = set()

        if working_hours:
            for value in self._build_time_range(working_hours.start_time, working_hours.end_time, slot_minutes):
                scheduled_times.add(value)

        booked_times = self.bookings.get(date, set())
        all_times = sorted(scheduled_times.union(booked_times))

        return [
            {
                "time": time,
                "available": (time in scheduled_times) and (time not in booked_times),
                "protected_booking": (time in booked_times) and (time not in scheduled_times),
            }
            for time in all_times
        ]

    def book_client(self, date: str, time: str) -> None:
        self._validate_date(date)
        self._validate_time(time)

        day_slots = self.list_slots(date)
        slot = next((item for item in day_slots if item["time"] == time), None)

        if not slot or not slot["available"]:
            raise ValueError(f"Time {time} is not available on {date}.")

        if date not in self.bookings:
            self.bookings[date] = set()

        self.bookings[date].add(time)

    def get_bookings(self, date: str) -> List[str]:
        self._validate_date(date)
        return sorted(self.bookings.get(date, set()))

    def _validate_day(self, day_of_week: int) -> None:
        if not isinstance(day_of_week, int) or day_of_week < 0 or day_of_week > 6:
            raise ValueError("day_of_week must be an integer from 0 (Mon) to 6 (Sun).")

    def _validate_date(self, date: str) -> None:
        if not isinstance(date, str):
            raise ValueError("date must be in YYYY-MM-DD format.")

        try:
            parsed = datetime.strptime(date, "%Y-%m-%d")
        except ValueError as error:
            raise ValueError("date must be a real calendar date in YYYY-MM-DD format.") from error

        if parsed.strftime("%Y-%m-%d") != date:
            raise ValueError("date must be a real calendar date in YYYY-MM-DD format.")

    def _validate_time(self, time: str) -> None:
        if not isinstance(time, str):
            raise ValueError("time must be in HH:MM 24-hour format.")

        try:
            datetime.strptime(time, "%H:%M")
        except ValueError as error:
            raise ValueError("time must be in HH:MM 24-hour format.") from error

    def _validate_range(self, start_time: str, end_time: str) -> None:
        self._validate_time(start_time)
        self._validate_time(end_time)

        if self._to_minutes(end_time) <= self._to_minutes(start_time):
            raise ValueError("end_time must be after start_time.")

    def _validate_slot_minutes(self, slot_minutes: int) -> None:
        if not isinstance(slot_minutes, int) or slot_minutes <= 0:
            raise ValueError("slot_minutes must be a positive integer.")

    def _get_day_of_week(self, date: str) -> int:
        parsed = datetime.strptime(date, "%Y-%m-%d")
        return parsed.weekday()

    def _to_minutes(self, time: str) -> int:
        hours, minutes = map(int, time.split(":"))
        return (hours * 60) + minutes

    def _to_time(self, total_minutes: int) -> str:
        hours = str(total_minutes // 60).zfill(2)
        minutes = str(total_minutes % 60).zfill(2)
        return f"{hours}:{minutes}"

    def _build_time_range(self, start_time: str, end_time: str, slot_minutes: int) -> List[str]:
        start = self._to_minutes(start_time)
        end = self._to_minutes(end_time)
        values: List[str] = []

        minute = start
        while minute + slot_minutes <= end:
            values.append(self._to_time(minute))
            minute += slot_minutes

        return values
