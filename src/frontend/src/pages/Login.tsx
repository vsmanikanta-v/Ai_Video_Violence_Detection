import { useState } from 'react'
import type { FormEvent } from 'react'
import { Link, useLocation, useNavigate } from 'react-router-dom'
import { apiLogin, type ApiError } from '@/api/client'
import { useAppDispatch } from '@/store/hooks'
import { setAuth } from '@/store/authSlice'

export function Login() {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)
  const dispatch = useAppDispatch()
  const navigate = useNavigate()
  const location = useLocation()
  const from = (location.state as { from?: { pathname: string } })?.from?.pathname ?? '/'

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    setError(null)
    setLoading(true)
    try {
      const res = await apiLogin({ username, password })
      dispatch(setAuth({ user: res.user, token: res.access_token }))
      navigate(from, { replace: true })
    } catch (err) {
      const apiErr = err as ApiError
      setError(apiErr.detail ?? 'Login failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-soft-cream">
      <header className="border-b border-soft-sage/30 bg-soft-sand/60 py-3">
        <div className="max-w-5xl mx-auto px-4 flex justify-between items-center">
          <Link to="/" className="font-semibold text-soft-navy">AI Video Violence Detection</Link>
          <Link to="/register" className="text-sm text-soft-slate hover:text-soft-navy">Register</Link>
        </div>
      </header>
      <main id="main-content" className="max-w-md mx-auto mt-12 px-4">
        <div className="rounded-xl border border-soft-sage/40 bg-white/60 p-8 shadow-sm">
        <h1 className="text-2xl font-semibold text-soft-navy mb-6">Login</h1>
        <form onSubmit={handleSubmit} className="space-y-4" aria-label="Login form">
          <div>
            <label htmlFor="login-username" className="block text-sm font-medium text-soft-slate mb-1">
              Username
            </label>
            <input
              id="login-username"
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
              autoComplete="username"
              aria-required="true"
              aria-describedby={error ? 'login-error' : undefined}
              className="w-full px-3 py-2 rounded-lg border border-soft-sage/50 bg-white focus:ring-2 focus:ring-soft-sage/50 focus:border-soft-sage"
            />
          </div>
          <div>
            <label htmlFor="login-password" className="block text-sm font-medium text-soft-slate mb-1">
              Password
            </label>
            <input
              id="login-password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              autoComplete="current-password"
              aria-required="true"
              aria-describedby={error ? 'login-error' : undefined}
              className="w-full px-3 py-2 rounded-lg border border-soft-sage/50 bg-white focus:ring-2 focus:ring-soft-sage/50 focus:border-soft-sage"
            />
          </div>
          {error && (
            <div id="login-error" role="alert" aria-live="assertive" className="text-sm text-red-600">
              {error}
            </div>
          )}
          <button
            type="submit"
            disabled={loading}
            aria-busy={loading}
            className="w-full py-2.5 rounded-lg bg-soft-sage/60 text-soft-navy font-medium hover:bg-soft-sage/80 disabled:opacity-50 transition"
          >
            {loading ? (
              <>
                <span className="sr-only">Signing in, please wait</span>
                <span aria-hidden="true">Signing in…</span>
              </>
            ) : (
              'Sign in'
            )}
          </button>
        </form>
        <p className="mt-4 text-sm text-soft-slate">
          Don&apos;t have an account?{' '}
          <Link to="/register" className="text-soft-navy font-medium hover:underline">
            Register
          </Link>
        </p>
        </div>
      </main>
    </div>
  )
}
