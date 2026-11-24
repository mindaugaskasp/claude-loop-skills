import { addPercent, type Cents } from './lib/money.js';
import { zoneFor, type Zone } from './lib/postcode.js';
import type { Grams } from './lib/weight.js';
import { basePrice, zoneSurcharge } from './rates.js';

export const VAT_PERCENT = 21;

export interface Quote {
  zone: Zone;
  net: Cents;
  total: Cents;
}

export function quoteFor(grams: Grams, postcode: string): Quote {
  const zone = zoneFor(postcode);
  const net = basePrice(grams) + zoneSurcharge(zone);
  return { zone, net, total: addPercent(net, VAT_PERCENT) };
}
