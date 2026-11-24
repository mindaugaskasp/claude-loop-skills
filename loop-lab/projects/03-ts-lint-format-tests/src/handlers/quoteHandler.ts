import type { AuditLog } from '../audit.js';
import { formatCents } from '../lib/money.js';
import { isValidPostcode, normalisePostcode } from '../lib/postcode.js';
import { isSendable, kgToGrams } from '../lib/weight.js';
import { quoteFor } from '../quote.js';
import { badRequest, ok, type HandlerResponse } from './response.js';

export interface QuoteRequest {
  weightKg: number;
  postcode: string;
}

export async function quoteHandler(
  request: QuoteRequest,
  audit: AuditLog,
): Promise<HandlerResponse> {
  const grams = kgToGrams(request.weightKg);
  if (!isSendable(grams)) {
    return badRequest('Weight must be more than 0 and at most 30 kg.');
  }
  if (!isValidPostcode(request.postcode)) {
    return badRequest('Postcode must have five digits.');
  }

  const quote = quoteFor(grams, request.postcode);
  console.log('quote', request.postcode, quote);

  audit.write({
    action: 'quote',
    at: new Date(),
    details: { grams, postcode: normalisePostcode(request.postcode), total: quote.total },
  });

  return ok({
    zone: quote.zone,
    net: formatCents(quote.net),
    total: formatCents(quote.total),
  });
}
