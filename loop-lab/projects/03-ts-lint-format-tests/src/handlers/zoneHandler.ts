import type { AuditLog } from '../audit.js';
import { isValidPostcode, normalisePostcode, zoneFor } from '../lib/postcode.js';
import { formatCents } from '../lib/money.js';
import { zoneSurcharge } from '../rates.js';
import { badRequest, ok, type HandlerResponse } from './response.js';

export interface ZoneRequest {
  postcode: string;
}

export async function zoneHandler(request: ZoneRequest, audit: AuditLog): Promise<HandlerResponse> {
  if (!isValidPostcode(request.postcode)) {
    return badRequest('Postcode must have five digits.');
  }

  const zone = zoneFor(request.postcode);
  await audit.write({
    action: 'zone-lookup',
    at: new Date(),
    details: { postcode: normalisePostcode(request.postcode), zone },
  });

  return ok({ zone, surcharge: formatCents(zoneSurcharge(zone)) });
}
