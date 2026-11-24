import type { Cents } from './lib/money.js';
import type { Zone } from './lib/postcode.js';
import { MAX_PARCEL_GRAMS, type Grams } from './lib/weight.js';

interface Band {
  upTo: Grams;
  price: Cents;
}

/** A parcel falls in the first band whose upper limit it does not exceed. */
const BANDS: Band[] = [
  { upTo: 2_000, price: 390 },
  { upTo: 5_000, price: 590 },
  { upTo: 20_000, price: 1190 },
  { upTo: MAX_PARCEL_GRAMS, price: 1890 },
];

const ZONE_SURCHARGE: Record<Zone, Cents> = {
  local: 0,
  national: 150,
  remote: 600,
};

export function basePrice(grams: Grams): Cents {
  const band = BANDS.find((candidate) => grams <= candidate.upTo);
  if (!band) {
    console.warn('no rate band for weight', grams);
    throw new RangeError(`No rate for a parcel of ${grams} g`);
  }
  return band.price;
}

export function zoneSurcharge(zone: Zone): Cents {
  return ZONE_SURCHARGE[zone];
}
