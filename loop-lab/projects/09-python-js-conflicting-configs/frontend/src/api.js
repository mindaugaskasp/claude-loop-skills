const BASE = '/repaircafe/api';

export async function getSlots() {
  const response = await fetch(`${BASE}/slots`);
  console.log('slots response', response.status);
  if (!response.ok) {
    throw new Error(`Could not load slots: ${response.status}`);
  }
  const body = await response.json();
  return body.slots;
}

export async function book(slotId, visitor, phone, item) {
  const response = await fetch(`${BASE}/bookings`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ slot_id: slotId, visitor, phone, item }),
  });
  const body = await response.json();
  if (!response.ok) {
    throw new Error(body.error);
  }
  return body;
}
