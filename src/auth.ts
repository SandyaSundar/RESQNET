import { create } from 'zustand'
import { api, ApiError, AUTH_ON, setUnauthorizedHandler } from './api'

export type User = { email: string; name: string; picture?: string }
type Status = 'loading' | 'in' | 'out'

const msg = (e: any) => {
  const s = e instanceof ApiError ? e.status : 0
  if (s === 401) return 'Sign-in could not be verified. Please try again.'
  if (s === 429) return e.message
  return 'Could not reach the server. It may be waking up, so please try again in a few seconds.'
}

export const useAuth = create<{
  status: Status; user: User | null; error: string
  init: () => Promise<void>; signIn: (credential: string) => Promise<void>; signOut: () => Promise<void>; clearError: () => void
}>((set) => ({
  status: AUTH_ON ? 'loading' : 'in', user: null, error: '',
  init: async () => {
    if (!AUTH_ON) return
    setUnauthorizedHandler(() => set({ status: 'out', user: null, error: 'Your session has expired. Please sign in again.' }))
    try { const u = await api.authMe(); set({ status: 'in', user: u?.user ?? u, error: '' }) }
    catch { set({ status: 'out', user: null }) } // no valid session yet: show login
  },
  signIn: async (credential) => {
    set({ status: 'loading', error: '' })
    try { const u = await api.authGoogle(credential); set({ status: 'in', user: u?.user ?? u }) }
    catch (e: any) { set({ status: 'out', user: null, error: msg(e) }) }
  },
  signOut: async () => {
    try { await api.authLogout() } catch { /* cookie expires server-side anyway */ }
    ;(window as any).google?.accounts?.id?.disableAutoSelect?.()
    set({ status: 'out', user: null, error: '' })
  },
  clearError: () => set({ error: '' }),
}))