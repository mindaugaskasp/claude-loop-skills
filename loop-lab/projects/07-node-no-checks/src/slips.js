'use strict';

const fs = require('node:fs/promises');
const path = require('node:path');
const config = require('./config');
const texts = require('./texts');

function escapeHtml(value) {
  return String(value)
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;');
}

function formatMoney(cents) {
  return `${Math.floor(cents / 100)}.${String(cents % 100).padStart(2, '0')} EUR`;
}

function renderSlip(order) {
  const rows = order.lines
    .map(
      (line) =>
        `<tr><td>${escapeHtml(line.sku)}</td><td>${escapeHtml(line.title)}</td>` +
        `<td>${line.glaze}</td><td>${line.quantity}</td>` +
        `<td>${formatMoney(line.priceCents * line.quantity)}</td></tr>`
    )
    .join('\n');
  const total = order.lines.reduce((sum, line) => sum + line.priceCents * line.quantity, 0);

  return `<!doctype html>
<html lang="en">
<head><meta charset="utf-8"><title>${texts.slipTitle} ${escapeHtml(order.id)}</title></head>
<body>
<h1>${texts.slipTitle} ${escapeHtml(order.id)}</h1>
<p>${escapeHtml(order.name)}<br>${order.address}</p>
<table>
<tr><th>Item</th><th>Piece</th><th>Glaze</th><th>Qty</th><th>Price</th></tr>
${rows}
</table>
<p>Total: ${formatMoney(total)}</p>
${order.note ? `<p><strong>${texts.slipNoteLabel}:</strong> ${escapeHtml(order.note)}</p>` : ''}
<p>${texts.slipThanks}</p>
</body>
</html>
`;
}

async function writeSlips(orders) {
  const dir = path.join(config.outDir, 'slips');
  await fs.mkdir(dir, { recursive: true });
  for (const order of orders) {
    fs.writeFile(path.join(dir, `${order.id}.html`), renderSlip(order));
  }
  return dir;
}

module.exports = { renderSlip, writeSlips, escapeHtml, formatMoney };
