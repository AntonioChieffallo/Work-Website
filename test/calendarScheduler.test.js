const test = require('node:test');
const assert = require('node:assert/strict');
const { CalendarScheduler } = require('../calendarScheduler');

test('uses recurring weekly hours to create available slots', () => {
  const scheduler = new CalendarScheduler();
  scheduler.setRecurringHours(1, '09:00', '10:00'); // Monday

  const slots = scheduler.listSlots('2026-09-21'); // Monday

  assert.deepEqual(slots, [
    { time: '09:00', available: true, protectedBooking: false },
    { time: '09:30', available: true, protectedBooking: false }
  ]);
});

test('date-specific override takes priority over recurring schedule', () => {
  const scheduler = new CalendarScheduler();
  scheduler.setRecurringHours(1, '09:00', '17:00');
  scheduler.setDateHours('2026-09-21', '13:00', '14:00');

  const slots = scheduler.listSlots('2026-09-21');

  assert.deepEqual(slots, [
    { time: '13:00', available: true, protectedBooking: false },
    { time: '13:30', available: true, protectedBooking: false }
  ]);
});

test('clients can only book currently available slots', () => {
  const scheduler = new CalendarScheduler();
  scheduler.setRecurringHours(1, '09:00', '10:00');

  scheduler.bookClient('2026-09-21', '09:30');

  const slots = scheduler.listSlots('2026-09-21');

  assert.equal(slots.find((slot) => slot.time === '09:30').available, false);
  assert.throws(() => scheduler.bookClient('2026-09-21', '09:30'), /not available/);
});

test('retrospective schedule changes preserve existing client bookings', () => {
  const scheduler = new CalendarScheduler();
  scheduler.setRecurringHours(1, '09:00', '17:00');
  scheduler.bookClient('2026-09-21', '16:30');

  scheduler.setRecurringHours(1, '09:00', '12:00');

  const slots = scheduler.listSlots('2026-09-21');

  assert.ok(slots.find((slot) => slot.time === '16:30'));
  assert.deepEqual(slots.find((slot) => slot.time === '16:30'), {
    time: '16:30',
    available: false,
    protectedBooking: true
  });
  assert.deepEqual(scheduler.getBookings('2026-09-21'), ['16:30']);
});
