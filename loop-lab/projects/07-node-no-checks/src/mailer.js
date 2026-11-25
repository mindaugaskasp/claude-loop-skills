'use strict';

const config = require('./config');
const texts = require('./texts');

async function send(to, subject, body) {
  const response = await fetch(config.mailApiUrl, {
    method: 'POST',
    headers: {
      authorization: `Bearer ${config.mailApiKey}`,
      'content-type': 'application/json',
    },
    body: JSON.stringify({ from: config.mailFrom, to, subject, text: body }),
  });
  if (!response.ok) {
    throw new Error(`The mail service refused the message for ${to}: ${response.status}`);
  }
}

// Tells every customer in the export that their order is packed.
async function notifyPacked(orders) {
  let sent = 0;
  for (const order of orders) {
    if (!order.email) continue;
    send(order.email, texts.packedSubject, texts.packedBody(order.name, order.id));
    sent += 1;
  }
  return sent;
}

module.exports = { send, notifyPacked };
