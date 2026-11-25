import { book, getSlots } from './api.js';
import { isFilled, slotLabel } from './format.js';
import { texts } from './texts.js';

function showMessage(root, text) {
  root.querySelector('.rc-message').textContent = text;
}

export async function mount(root) {
  showMessage(root, texts.loading);
  const slots = await getSlots();
  const select = root.querySelector('select[name=slot]');
  for (const slot of slots) {
    const option = document.createElement('option');
    option.value = slot.id;
    option.textContent = slotLabel(slot);
    select.append(option);
  }
  showMessage(root, slots.length === 0 ? texts.noSlots : '');

  root.querySelector('form').addEventListener('submit', async (event) => {
    event.preventDefault();
    const form = new window.FormData(event.target);
    const visitor = form.get('visitor');
    const phone = form.get('phone');
    if (!isFilled(visitor)) {
      showMessage(root, texts.missingName);
      return;
    }
    if (!isFilled(phone)) {
      showMessage(root, texts.missingPhone);
      return;
    }
    try {
      const booking = await book(form.get('slot'), visitor, phone, form.get('item'));
      console.log('booked', booking);
      showMessage(root, texts.booked);
    } catch (error) {
      showMessage(root, error.message || texts.failed);
    }
  });
}
