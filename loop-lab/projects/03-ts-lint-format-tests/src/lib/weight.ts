export type Grams = number;

export const MAX_PARCEL_GRAMS: Grams = 30_000;

export function kgToGrams(kg: number): Grams {
  return Math.round(kg * 1000);
}

/** 2500 becomes "2.5 kg". */
export function formatWeight(grams: Grams): string {
  return `${grams / 1000} kg`;
}

export function isSendable(grams: Grams): boolean {
  return Number.isFinite(grams) && grams > 0 && grams <= MAX_PARCEL_GRAMS;
}
