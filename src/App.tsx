import { useEffect, useState } from 'react'
import { NavLink, Route, Routes } from 'react-router-dom'
import { useStore } from './store'
import { AUTH_ON } from './api'
import { useAuth } from './auth'
import RequireAuth from './components/RequireAuth'
import ThemeToggle from './components/ThemeToggle'
import ProfileMenu from './components/ProfileMenu'
import Home from './pages/Home'
import Scenarios from './pages/Scenarios'
import Mission from './pages/Mission'
import Experiments from './pages/Experiments'
import Analytics from './pages/Analytics'
import Settings from './pages/Settings'

const tabs = [['/', 'HOME'], ['/mission', 'MISSION CONTROL'], ['/scenarios', 'SCENARIOS'], ['/experiments', 'EXPERIMENTS'], ['/analytics', 'ANALYTICS'], ['/settings', 'SETTINGS']]
export default function App() {
  const boot = useStore((s) => s.boot); const run = useStore((s) => s.run); const warming = useStore((s) => s.warming)
  const { status, init } = useAuth()
  const [now, setNow] = useState(new Date())
  useEffect(() => { init() }, [])
  useEffect(() => { if (status === 'in') boot() }, [status]) // load data only once signed in
  useEffect(() => { const t = setInterval(() => setNow(new Date()), 1000); return () => clearInterval(t) }, [])
  const signedIn = !AUTH_ON || status === 'in'
  return (
    <div className="app">
      <header className="top">
        <div className="brand">
          <img src="/favicon.png" alt="RESQNET logo" className="brand-logo" />
          <span className="brand-name">RESQ<b>NET</b></span>
          <small>MISSION CONTROL</small>
        </div>
        <div className="sep" />
        {signedIn && <nav>{tabs.map(([to, l]) => <NavLink key={to} to={to} end={to === '/'} className={({ isActive }) => (isActive ? 'on' : '')}>{l}</NavLink>)}</nav>}
        {!signedIn && <div style={{ flex: 1 }} />}
        <div className="top-r">
          {signedIn && <><span className="mono mut">{run ? `TICK ${run.tick}` : 'NO RUN'}</span>
          <span className="clock mono">{now.toLocaleTimeString('en-GB')}</span></>}
          <ThemeToggle />
          <ProfileMenu />
        </div>
      </header>
      {signedIn && warming && <div className="note" role="status">Syncing live data from the server. The first load can take up to a minute.</div>}
      <main>
        <RequireAuth>
          <Routes>
            <Route path="/" element={<Home />} /><Route path="/scenarios" element={<Scenarios />} />
            <Route path="/mission" element={<Mission />} /><Route path="/experiments" element={<Experiments />} />
            <Route path="/analytics" element={<Analytics />} /><Route path="/settings" element={<Settings />} />
          </Routes>
        </RequireAuth>
      </main>
    </div>
  )
}