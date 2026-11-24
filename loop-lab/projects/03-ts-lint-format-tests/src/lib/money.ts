/** All amounts are whole cents. */
export type Cents = number;

/** Rounds half up to a whole cent. */
export function roundToCents(amount: number): Cents {
  return Math.round(amount);
}

/** Adds a percentage (for example VAT) to an amount and rounds to a whole cent. */
export function addPercent(amount: Cents, percent: number): Cents {
  return roundToCents(amount * (1 + percent / 100));
}

/** 1250 becomes "12.50". */
export function formatCents(amount: Cents): string {
  const sign = amount < 0 ? '-' : '';
  const abs = Math.abs(amount);
  const euros = Math.floor(abs / 100);
  const cents = String(abs % 100).padStart(2, '0');
  return `${sign}${euros}.${cents}`;
}
