import { describe, expect, it } from 'vitest';
import { basePrice, zoneSurcharge } from '../src/rates.js';

describe('basePrice', () => {
  it('uses the first band a parcel fits in', () => {
    expect(basePrice(500)).toBe(390);
    expect(basePrice(3_000)).toBe(590);
    expect(basePrice(12_000)).toBe(1190);
  });

  it('treats a band limit as still inside the band', () => {
    expect(basePrice(2_000)).toBe(390);
    expect(basePrice(2_001)).toBe(590);
  });
});

describe('zoneSurcharge', () => {
  it('charges nothing extra for local parcels', () => {
    expect(zoneSurcharge('local')).toBe(0);
  });
});
