from __future__ import annotations

from typing import List, Dict, Any

from calendar_scheduler import CalendarScheduler


def build_demo_scheduler() -> CalendarScheduler:
    scheduler = CalendarScheduler()
    scheduler.set_recurring_hours(0, "09:00", "17:00")
    scheduler.book_client("2026-09-21", "16:30")
    scheduler.set_recurring_hours(0, "09:00", "12:00")
    return scheduler


def list_available_slots(scheduler: CalendarScheduler, date: str) -> List[Dict[str, Any]]:
    return scheduler.list_slots(date)


def book_client_for_date(scheduler: CalendarScheduler, date: str, time: str) -> List[str]:
    scheduler.book_client(date, time)
    return scheduler.get_bookings(date)
