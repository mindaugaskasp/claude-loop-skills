'use strict';

const fs = require('node:fs/promises');
const path = require('node:path');
const config = require('./config');

// Groups made-to-order pieces by glaze and fills firings up to the kiln's capacity.
function planFirings(orders, capacity = config.kilnCapacity) {
  const byGlaze = new Map();
  for (const order of orders) {
    for (const line of order.lines) {
      if (!line.madeToOrder) continue;
      const list = byGlaze.get(line.glaze) || [];
      list.push({ orderId: order.id, sku: line.sku, title: line.title, units: line.shelfUnits * line.quantity });
      byGlaze.set(line.glaze, list);
    }
  }

  const firings = [];
  for (const [glaze, pieces] of byGlaze) {
    let current = { glaze, units: 0, pieces: [] };
    for (const piece of pieces) {
      if (current.units + piece.units > capacity && current.pieces.length > 0) {
        firings.push(current);
        current = { glaze, units: 0, pieces: [] };
      }
      current.pieces.push(piece);
      current.units += piece.units;
    }
    if (current.pieces.length > 0) firings.push(current);
  }
  return firings;
}

function renderPlan(firings) {
  return firings
    .map((firing, i) => {
      const lines = firing.pieces.map((p) => `  ${p.orderId}  ${p.sku}  ${p.title} (${p.units})`);
      return [`Firing ${i + 1}: ${firing.glaze}, ${firing.units} shelf units`, ...lines].join('\n');
    })
    .join('\n\n');
}

async function writePlan(firings) {
  const file = path.join(config.outDir, 'kiln-plan.txt');
  try {
    await fs.mkdir(config.outDir, { recursive: true });
    await fs.writeFile(file, renderPlan(firings) + '\n');
  } catch (err) {
    // ignore
  }
  return file;
}

module.exports = { planFirings, renderPlan, writePlan };
