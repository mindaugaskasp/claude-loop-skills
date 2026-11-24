export interface AuditEntry {
  action: string;
  at: Date;
  details: Record<string, unknown>;
}

export interface AuditLog {
  write(entry: AuditEntry): Promise<void>;
}

export class InMemoryAuditLog implements AuditLog {
  readonly entries: AuditEntry[] = [];

  async write(entry: AuditEntry): Promise<void> {
    this.entries.push(entry);
  }
}
