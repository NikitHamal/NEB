import type { Request as ExpressRequest } from "express";
import type { Socket } from "socket.io";

// Bridges an Express request into a Fetch API Request, which @clerk/backend expects. Pass `body` only for the raw-body webhook route.
export function toFetchRequest(req: ExpressRequest, body?: Buffer): Request {
  const host = req.get("host") ?? "localhost";
  const url = `${req.protocol}://${host}${req.originalUrl}`;

  const headers = new Headers();
  for (const [key, value] of Object.entries(req.headers)) {
    if (value === undefined) continue;
    if (Array.isArray(value)) {
      for (const item of value) headers.append(key, item);
    } else {
      headers.set(key, value);
    }
  }

  const canHaveBody = body !== undefined && req.method !== "GET" && req.method !== "HEAD";

  return new Request(url, {
    method: req.method,
    headers,
    ...(canHaveBody ? { body } : {}),
  });
}

// Same idea, from a socket.io handshake instead of an HTTP request - the client sends its Clerk
// session token via `auth.token` (there's no cookie/header exchange in a WS handshake to piggyback on).
export function toSocketFetchRequest(client: Socket): Request {
  const origin = client.handshake.headers.origin ?? "http://localhost";
  const token = client.handshake.auth?.token as string | undefined;

  const headers = new Headers();
  if (token) {
    headers.set("Authorization", `Bearer ${token}`);
  }

  return new Request(origin, { headers });
}
