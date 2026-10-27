import { useEffect, useRef, useState } from 'react'
import { CLIENT_ID } from '../api'
import { useAuth } from '../auth'
import { useTheme } from '../theme'

declare global { interface Window { google?: any } }
const SRC = 'https://accounts.google.com/gsi/client'

export default function Login() {
  const { signIn, error, clearError } = useAuth(); const mode = useTheme((s) => s.mode)
  const box = useRef<HTMLDivElement>(null); const [ready, setReady] = useState(!!window.google?.accounts)
  const [failed, setFailed] = useState(false)

  useEffect(() => {
    if (window.google?.accounts) { setReady(true); return }
    const s = document.createElement('script'); s.src = SRC; s.async = true; s.defer = true
    s.onload = () => setReady(true); s.onerror = () => setFailed(true)
    document.head.appendChild(s)
  }, [])

  useEffect(() => {
    if (!ready || !box.current || !window.google?.accounts) return
    window.google.accounts.id.initialize({ client_id: CLIENT_ID, callback: (r: any) => r?.credential && signIn(r.credential), auto_select: false, cancel_on_tap_outside: true })
    box.current.innerHTML = ''
    window.google.accounts.id.renderButton(box.current, { theme: mode === 'dark' ? 'filled_black' : 'outline', size: 'large', shape: 'pill', text: 'signin_with', width: 280 })
  }, [ready, mode])

  return (
    <div className="authwrap">
      <div className="card authcard">
        <img src="/favicon.png" alt="RESQNET" className="authlogo" />
        <h1>RESQ<b>NET</b></h1>
        <p className="sub">Resilient Swarm Coordination for Disaster Response</p>
        <p className="mut" style={{ margin: '18px 0 14px' }}>Sign in with your Google account to continue.</p>
        <div ref={box} className="gbtn" />
        {!ready && !failed && <p className="mut">Loading Google Sign-In…</p>}
        {failed && <div className="err" style={{ marginTop: 12 }}>Google Sign-In could not be loaded. Check your connection and refresh.</div>}
        {error && <div className="err" style={{ marginTop: 12 }} role="alert" onClick={clearError}>{error}</div>}
        <p className="mut" style={{ fontSize: 11, marginTop: 18 }}>Secure sign-in with Google. RESQNET never sees or stores your password.</p>
      </div>
    </div>
  )
}