const BASE_URL = import.meta.env.VITE_BACKEND_URL || '';
export const CLIENT_ID = import.meta.env.VITE_GOOGLE_CLIENT_ID as string | undefined
export const AUTH_ON = !!CLIENT_ID
// Cookies are only sent when auth is enabled (credentialed CORS needs an explicit allowed origin on the backend).
const CRED: RequestCredentials = AUTH_ON ? 'include' : 'same-origin'

export class ApiError extends Error {
  status: number; retryAfter?: number
  constructor(m: string, status: number, retryAfter?: number) { super(m); this.status = status; this.retryAfter = retryAfter }
}
let onUnauth: (() => void) | null = null
export const setUnauthorizedHandler = (f: (() => void) | null) => { onUnauth = f }

let refreshing: Promise<boolean> | null = null
const refresh = () => (refreshing ??= fetch(`${BASE_URL}/api/auth/refresh`, { method: 'POST', credentials: CRED })
  .then((r) => r.ok).catch(() => false).finally(() => { refreshing = null }))

// Everything comes from the RESQNET backend. In dev, Vite can fall back to local proxy if VITE_BACKEND_URL is unset.
async function req(path: string, init?: RequestInit, retried = false): Promise<any> {
  const r = await fetch(`${BASE_URL}${path}`, { ...init, credentials: CRED, headers: { 'Content-Type': 'application/json' } })
  let body: any = null
  try { body = await r.json() } catch { /* empty */ }
  if (r.status === 401 && AUTH_ON && !path.startsWith('/api/auth/')) {
    if (!retried && (await refresh())) return req(path, init, true) // session renewed, retry once
    onUnauth?.() // refresh failed: session expired
  }
  if (r.status === 429) {
    const ra = Number(r.headers.get('Retry-After')) || undefined
    throw new ApiError(ra ? `Too many requests. Please wait ${ra}s and try again.` : 'Too many requests. Please wait a moment and try again.', 429, ra)
  }
  if (!r.ok) throw new ApiError(`${r.status} ${typeof body?.detail === 'string' ? body.detail : r.statusText}`, r.status)
  return body
}

export const api = {
  // /api/health also pings PostgreSQL and can answer 503 (DB down) or hang. Never let that block the app: 5 s timeout.
  health: async () => {
    const ctl = new AbortController(); const t = setTimeout(() => ctl.abort(), 5000)
    try { const r = await fetch(`${BASE_URL}/api/health`, { signal: ctl.signal }); try { return await r.json() } catch { return { status: 'unhealthy' } } }
    finally { clearTimeout(t) }
  },
  scenarios: () => req('/api/simulations/scenarios'),
  create: (scenario_id: string, mode?: string) => req('/api/simulations', { method: 'POST', body: JSON.stringify({ scenario_id, mode }) }),
  tick: (id: string, ticks = 1) => req(`/api/simulations/${id}/ticks`, { method: 'POST', body: JSON.stringify({ ticks }) }),
  state: (id: string) => req(`/api/simulations/${id}`),
  droneConfig: () => req('/api/datasets/drone-config'),
  failureScenarios: () => req('/api/datasets/failure-scenarios'),
  // Not implemented by the backend: its real response/error is surfaced in the UI, never faked.
  inject: (id: string, type: string, payload: any = {}) => req(`/api/simulations/${id}/failures`, { method: 'POST', body: JSON.stringify({ type, ...payload }) }),
  // Auth: the backend verifies the Google ID token and sets an HttpOnly session cookie.
  authGoogle: (credential: string) => req('/api/auth/google', { method: 'POST', body: JSON.stringify({ credential }) }),
  authMe: () => req('/api/auth/me'),
  authLogout: () => req('/api/auth/logout', { method: 'POST' }),
}