import { AUTH_ON } from '../api'
import { useAuth } from '../auth'
import Login from '../pages/Login'

// Guards everything inside it. Auth off => children render as before.
export default function RequireAuth({ children }: { children: any }) {
  const status = useAuth((s) => s.status)
  if (!AUTH_ON || status === 'in') return <>{children}</>
  if (status === 'loading') return <div className="authwrap"><div className="note" role="status">Connecting securely…</div></div>
  return <Login />
}