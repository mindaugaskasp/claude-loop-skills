import { describe, expect, it } from 'vitest';
import { InMemoryAuditLog } from '../src/audit.js';
import { quoteHandler } from '../src/handlers/quoteHandler.js';

describe('quoteHandler', () => {
  it('quotes a small national parcel', async () => {
    const audit = new InMemoryAuditLog();
    const response = await quoteHandler({ weightKg: 1.2, postcode: 'LT-44280' }, audit);

    expect(response.status).toBe(200);
    expect(response.body).toEqual({ zone: 'national', net: '5.40', total: '6.53' });
    expect(audit.entries).toHaveLength(1);
  });

  it('rejects a parcel that is too heavy', async () => {
    const response = await quoteHandler(
      { weightKg: 31, postcode: '01103' },
      new InMemoryAuditLog(),
    );

    expect(response.status).toBe(400);
  });
});
