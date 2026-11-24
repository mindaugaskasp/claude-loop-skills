export type Zone = 'local' | 'national' | 'remote';

const REMOTE_PREFIXES = ['93', '94', '99'];
const LOCAL_PREFIXES = ['01', '02', '03'];

/** Removes spaces and a leading country code: " lt-01103 " becomes "01103". */
export function normalisePostcode(input: string): string {
  return input.trim().toUpperCase().replace(/^LT-?/, '').replace(/\s+/g, '');
}

export function isValidPostcode(input: string): boolean {
  return /^\d{5}$/.test(normalisePostcode(input));
}

export function zoneFor(postcode: string): Zone {
  const prefix = normalisePostcode(postcode).slice(0, 2);
  if (LOCAL_PREFIXES.includes(prefix)) {
    return 'local';
  }
  if (REMOTE_PREFIXES.includes(prefix)) {
    return 'remote';
  }
  return 'national';
}
