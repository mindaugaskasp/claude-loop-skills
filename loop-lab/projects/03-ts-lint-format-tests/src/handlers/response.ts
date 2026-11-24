export interface HandlerResponse {
  status: number;
  body: Record<string, unknown>;
}

export function ok(body: Record<string, unknown>): HandlerResponse {
  return { status: 200, body };
}

export function badRequest(message: string): HandlerResponse {
  return { status: 400, body: { error: message } };
}
