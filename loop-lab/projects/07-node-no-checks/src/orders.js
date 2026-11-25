'use strict';

const fs = require('node:fs/promises');

// Splits one CSV line. Fields may be wrapped in double quotes; a quote inside
// a quoted field is written twice.
function splitLine(line) {
  const fields = [];
  let current = '';
  let quoted = false;
  for (let i = 0; i < line.length; i += 1) {
    const ch = line[i];
    if (quoted) {
      if (ch === '"' && line[i + 1] === '"') {
        current += '"';
        i += 1;
      } else if (ch === '"') {
        quoted = false;
      } else {
        current += ch;
      }
    } else if (ch === '"') {
      quoted = true;
    } else if (ch === ',') {
      fields.push(current);
      current = '';
    } else {
      current += ch;
    }
  }
  fields.push(current);
  return fields;
}

function toCents(text) {
  const [whole, part = ''] = String(text).trim().split('.');
  return Number(whole) * 100 + Number((part + '00').slice(0, 2));
}

// Reads the webshop export and returns one object per order, with its lines.
async function readOrders(file) {
  const text = await fs.readFile(file, 'utf8');
  const rows = text.split(/\r?\n/).filter((row) => row.trim() !== '');
  const header = splitLine(rows[0]);
  const orders = new Map();

  for (const row of rows.slice(1)) {
    const values = splitLine(row);
    const record = Object.fromEntries(header.map((name, i) => [name, values[i] ?? '']));
    let quantity = 1;
    try {
      quantity = parseInt(record.quantity, 10);
    } catch (err) {}

    if (!orders.has(record.order_id)) {
      orders.set(record.order_id, {
        id: record.order_id,
        name: record.customer_name,
        email: record.customer_email,
        address: record.address,
        note: record.note,
        lines: [],
      });
    }
    orders.get(record.order_id).lines.push({
      sku: record.sku,
      title: record.title,
      quantity,
      priceCents: toCents(record.unit_price),
      glaze: record.glaze,
      shelfUnits: Number(record.shelf_units || 1),
      madeToOrder: record.made_to_order === 'yes',
    });
  }
  return [...orders.values()];
}

module.exports = { readOrders, splitLine, toCents };
