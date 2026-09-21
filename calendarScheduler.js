class CalendarScheduler {
  constructor() {
    this.weeklyHours = new Map();
    this.dateOverrides = new Map();
    this.bookings = new Map();
  }

  setRecurringHours(dayOfWeek, startTime, endTime) {
    this.#validateDay(dayOfWeek);
    this.#validateRange(startTime, endTime);
    this.weeklyHours.set(dayOfWeek, { startTime, endTime });
  }

  clearRecurringHours(dayOfWeek) {
    this.#validateDay(dayOfWeek);
    this.weeklyHours.delete(dayOfWeek);
  }

  setDateHours(date, startTime, endTime) {
    this.#validateDate(date);
    this.#validateRange(startTime, endTime);
    this.dateOverrides.set(date, { startTime, endTime });
  }

  setDateClosed(date) {
    this.#validateDate(date);
    this.dateOverrides.set(date, null);
  }

  clearDateOverride(date) {
    this.#validateDate(date);
    this.dateOverrides.delete(date);
  }

  getWorkingHours(date) {
    this.#validateDate(date);

    if (this.dateOverrides.has(date)) {
      return this.dateOverrides.get(date);
    }

    const dayOfWeek = this.#getDayOfWeek(date);
    return this.weeklyHours.get(dayOfWeek) ?? null;
  }

  listSlots(date, slotMinutes = 30) {
    this.#validateDate(date);
    this.#validateSlotMinutes(slotMinutes);

    const workingHours = this.getWorkingHours(date);
    const scheduledTimes = new Set();

    if (workingHours) {
      for (const time of this.#buildTimeRange(workingHours.startTime, workingHours.endTime, slotMinutes)) {
        scheduledTimes.add(time);
      }
    }

    const bookedTimes = this.bookings.get(date) ?? new Set();
    const allTimes = new Set([...scheduledTimes, ...bookedTimes]);

    return [...allTimes]
      .sort()
      .map((time) => ({
        time,
        available: scheduledTimes.has(time) && !bookedTimes.has(time),
        protectedBooking: bookedTimes.has(time) && !scheduledTimes.has(time)
      }));
  }

  bookClient(date, time) {
    this.#validateDate(date);
    this.#validateTime(time);

    const daySlots = this.listSlots(date);
    const slot = daySlots.find((item) => item.time === time);

    if (!slot || !slot.available) {
      throw new Error(`Time ${time} is not available on ${date}.`);
    }

    if (!this.bookings.has(date)) {
      this.bookings.set(date, new Set());
    }

    this.bookings.get(date).add(time);
  }

  getBookings(date) {
    this.#validateDate(date);
    return [...(this.bookings.get(date) ?? new Set())].sort();
  }

  #validateDay(dayOfWeek) {
    if (!Number.isInteger(dayOfWeek) || dayOfWeek < 0 || dayOfWeek > 6) {
      throw new Error('dayOfWeek must be an integer from 0 (Sun) to 6 (Sat).');
    }
  }

  #validateDate(date) {
    if (!/^\d{4}-\d{2}-\d{2}$/.test(date)) {
      throw new Error('date must be in YYYY-MM-DD format.');
    }

    const parsedDate = new Date(`${date}T00:00:00Z`);
    if (Number.isNaN(parsedDate.getTime()) || parsedDate.toISOString().slice(0, 10) !== date) {
      throw new Error('date must be a real calendar date in YYYY-MM-DD format.');
    }
  }

  #validateTime(time) {
    if (!/^([01]\d|2[0-3]):[0-5]\d$/.test(time)) {
      throw new Error('time must be in HH:MM 24-hour format.');
    }
  }

  #validateRange(startTime, endTime) {
    this.#validateTime(startTime);
    this.#validateTime(endTime);

    if (this.#toMinutes(endTime) <= this.#toMinutes(startTime)) {
      throw new Error('endTime must be after startTime.');
    }
  }

  #validateSlotMinutes(slotMinutes) {
    if (!Number.isInteger(slotMinutes) || slotMinutes <= 0) {
      throw new Error('slotMinutes must be a positive integer.');
    }
  }

  #getDayOfWeek(date) {
    return new Date(`${date}T00:00:00Z`).getUTCDay();
  }

  #toMinutes(time) {
    const [hours, minutes] = time.split(':').map(Number);
    return hours * 60 + minutes;
  }

  #toTime(totalMinutes) {
    const hours = String(Math.floor(totalMinutes / 60)).padStart(2, '0');
    const minutes = String(totalMinutes % 60).padStart(2, '0');
    return `${hours}:${minutes}`;
  }

  #buildTimeRange(startTime, endTime, slotMinutes) {
    const start = this.#toMinutes(startTime);
    const end = this.#toMinutes(endTime);
    const range = [];

    for (let minute = start; minute + slotMinutes <= end; minute += slotMinutes) {
      range.push(this.#toTime(minute));
    }

    return range;
  }
}

module.exports = {
  CalendarScheduler
};
