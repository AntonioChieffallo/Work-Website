from calendar_scheduler import CalendarScheduler


def build_demo_output() -> str:
    scheduler = CalendarScheduler()

    # Monday recurring hours
    scheduler.set_recurring_hours(0, "09:00", "17:00")

    date = "2026-09-21"
    scheduler.book_client(date, "16:30")

    # Business owner shortens Monday hours after booking already exists.
    scheduler.set_recurring_hours(0, "09:00", "12:00")

    slots = scheduler.list_slots(date)
    protected = [slot for slot in slots if slot["protected_booking"]]

    lines = [
        "Calendar Scheduler Demo",
        f"Date: {date}",
        f"Bookings: {', '.join(scheduler.get_bookings(date))}",
        f"Protected bookings after schedule change: {len(protected)}",
    ]

    if protected:
        lines.append(f"Protected time: {protected[0]['time']}")

    return "\n".join(lines)


def main() -> None:
    print(build_demo_output())


if __name__ == "__main__":
    main()
