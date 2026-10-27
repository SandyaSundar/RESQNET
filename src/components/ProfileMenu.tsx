import { useEffect, useRef, useState } from 'react'
import { AUTH_ON } from '../api'
import { useAuth } from '../auth'

export default function ProfileMenu() {
  const { status, user, signOut } = useAuth()
  const [open, setOpen] = useState(false)
  const ref = useRef<HTMLDivElement>(null)

  useEffect(() => {
    if (!open) return
    const onDown = (e: MouseEvent) => { if (ref.current && !ref.current.contains(e.target as Node)) setOpen(false) }
    const onKey = (e: KeyboardEvent) => { if (e.key === 'Escape') setOpen(false) }
    document.addEventListener('mousedown', onDown); document.addEventListener('keydown', onKey)
    return () => { document.removeEventListener('mousedown', onDown); document.removeEventListener('keydown', onKey) }
  }, [open])

  const signedIn = AUTH_ON && status === 'in' && !!user
  const Avatar = ({ big }: { big?: boolean }) => user?.picture
    ? <img className={'pav' + (big ? ' big' : '')} src={user.picture} alt="" referrerPolicy="no-referrer" />
    : <span className={'pav' + (big ? ' big' : '')}>{signedIn ? (user!.name?.[0] ?? '?').toUpperCase() : (
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><circle cx="12" cy="8" r="4" /><path d="M4 21c0-4.4 3.6-7 8-7s8 2.6 8 7" /></svg>)}</span>

  return (
    <div className="profile" ref={ref}>
      <button className="pbtn" onClick={() => setOpen((v) => !v)} aria-haspopup="menu" aria-expanded={open} title="Profile">
        <Avatar />
        <span className="pname">{signedIn ? user!.name : 'Profile'}</span>
        <span className="caret">▾</span>
      </button>
      {open && <div className="pmenu" role="menu">
        {signedIn ? <>
          <div className="phead"><Avatar big /><div><b>{user!.name}</b><span className="mut">{user!.email}</span></div></div>
          <button className="pitem" role="menuitem" onClick={() => { setOpen(false); signOut() }}>Sign out</button>
        </> : <>
          <div className="pnote">
            {AUTH_ON ? 'You are signed out. Use the Google button on the page to sign in.' : 'Guest mode. Google sign-in is not enabled on this deployment.'}
          </div>
        </>}
      </div>}
    </div>
  )
}