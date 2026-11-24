import { describe, expect, it } from 'vitest';
import { addPercent, formatCents } from '../src/lib/money.js';

describe('formatCents', () => {
  it('pads cents to two digits', () => {
    expect(formatCents(1205)).toBe('12.05');
  });

  it('keeps the sign for refunds', () => {
    expect(formatCents(-390)).toBe('-3.90');
  });
});

describe('addPercent', () => {
  it('rounds to a whole cent', () => {
    expect(addPercent(390, 21)).toBe(472);
  });
});
