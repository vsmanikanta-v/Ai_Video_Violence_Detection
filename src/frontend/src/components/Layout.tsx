import type { ReactNode } from 'react'
import { Link, useNavigate, Outlet } from 'react-router-dom'
import { useAppDispatch, useAppSelector } from '@/store/hooks'
import { clearAuth } from '@/store/authSlice'

interface LayoutProps {
  /** When provided, renders as the main content instead of the router Outlet. */
  children?: ReactNode
}

export function Layout({ children }: LayoutProps) {
  const { user, token } = useAppSelector((s) => s.auth)
  const dispatch = useAppDispatch()
  const navigate = useNavigate()

  const handleLogout = () => {
    dispatch(clearAuth())
    navigate('/login')
  }

  return (
    <div className="min-h-screen flex flex-col bg-soft-cream">
      <header className="bg-soft-sand border-b border-soft-sage/30 shadow-sm">
        <div className="max-w-5xl mx-auto px-4 py-3 flex items-center justify-between">
          <Link to="/" className="text-xl font-semibold text-soft-navy hover:text-soft-slate">
            AI Video Violence Detection
          </Link>
          <nav aria-label="Main navigation" className="flex items-center gap-4">
            {token ? (
              <>
                <Link to="/upload" className="text-soft-slate hover:text-soft-navy">Upload</Link>
                <Link to="/history" className="text-soft-slate hover:text-soft-navy">History</Link>
                {user?.role === 'ADMIN' && (
                  <Link to="/admin" className="text-soft-slate hover:text-soft-navy">Dashboard</Link>
                )}
                <span
                  className="inline-flex h-8 w-8 items-center justify-center rounded-full border border-soft-sage/40 bg-soft-sage/20 text-soft-navy"
                  title={user?.username ?? 'User'}
                  aria-label={`Signed in as ${user?.username ?? 'User'}`}
                >
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    strokeWidth="1.8"
                    className="h-4 w-4"
                    aria-hidden="true"
                  >
                    <circle cx="12" cy="8" r="3.25" />
                    <path d="M5.5 19.25c0-3.1 2.9-5.25 6.5-5.25s6.5 2.15 6.5 5.25" />
                  </svg>
                  <span className="sr-only">{user?.username ?? 'User'}</span>
                </span>
                <button
                  type="button"
                  onClick={handleLogout}
                  className="px-3 py-1.5 rounded-md bg-soft-coral/20 text-soft-navy hover:bg-soft-coral/30 transition"
                >
                  Logout
                </button>
              </>
            ) : (
              <>
                <Link to="/login" className="text-soft-slate hover:text-soft-navy">Login</Link>
                <Link to="/register" className="px-3 py-1.5 rounded-md bg-soft-sage/40 text-soft-navy hover:bg-soft-sage/60 transition">
                  Register
                </Link>
              </>
            )}
          </nav>
        </div>
      </header>
      <main id="main-content" className="flex-1 max-w-5xl w-full mx-auto px-4 py-6">
        {children ?? <Outlet />}
      </main>
    </div>
  )
}
