const timeFormat = new Intl.DateTimeFormat('en-GB', {
  weekday: 'short',
  hour: '2-digit',
  minute: '2-digit',
  timeZone: 'Europe/Vilnius',
});

export function slotLabel(slot) {
  return `${timeFormat.format(new Date(slot.starts_at))} - ${slot.skill}`;
}

export function isFilled(value) {
  return typeof value === 'string' && value.trim() !== '';
}
