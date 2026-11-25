#!/usr/bin/env node
'use strict';

const { readOrders } = require('../src/orders');
const { writeSlips } = require('../src/slips');
const { planFirings, renderPlan, writePlan } = require('../src/plan');
const { notifyPacked } = require('../src/mailer');

const usage = `Usage:
  kiln-desk slips  <orders.csv>   write one packing slip per order
  kiln-desk plan   <orders.csv>   print and save the kiln plan
  kiln-desk notify <orders.csv>   email customers that their order is packed`;

async function main() {
  const [command, file] = process.argv.slice(2);
  if (!command || !file) {
    console.log(usage);
    process.exitCode = 1;
    return;
  }

  const orders = await readOrders(file);

  if (command === 'slips') {
    const dir = await writeSlips(orders);
    console.log(`${orders.length} packing slips written to ${dir}`);
  } else if (command === 'plan') {
    const firings = planFirings(orders);
    console.log(renderPlan(firings));
    const saved = await writePlan(firings);
    console.log(`\nSaved to ${saved}`);
  } else if (command === 'notify') {
    const sent = await notifyPacked(orders);
    console.log(`${sent} customers notified`);
  } else {
    console.log(usage);
    process.exitCode = 1;
  }
}

main().catch((err) => {
  console.error(err.message);
  process.exitCode = 1;
});
