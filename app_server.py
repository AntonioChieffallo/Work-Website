from __future__ import annotations

from typing import List, Dict, Any

from calendar_scheduler import CalendarScheduler


def build_demo_scheduler() -> CalendarScheduler:
    scheduler = CalendarScheduler()
    for day_of_week in range(5):
        scheduler.set_recurring_hours(day_of_week, "09:00", "17:00")
    scheduler.book_client("2026-09-21", "16:30")
    return scheduler


def list_available_slots(scheduler: CalendarScheduler, date: str) -> List[Dict[str, Any]]:
    return scheduler.list_slots(date, slot_minutes=60)


def book_client_for_date(scheduler: CalendarScheduler, date: str, time: str) -> List[str]:
    scheduler.book_client(date, time)
    return scheduler.get_bookings(date)
