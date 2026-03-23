import { useState } from 'react'
import type { FormEvent } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { apiRegister, type ApiError } from '@/api/client'
import { useAppDispatch } from '@/store/hooks'
import { setAuth } from '@/store/authSlice'

export function Register() {
  const [username, setUsername] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)
  const dispatch = useAppDispatch()
  const navigate = useNavigate()

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    setError(null)
    setLoading(true)
    try {
      const res = await apiRegister({ username, email, password, role: 'USER' })
      dispatch(setAuth({ user: res.user, token: res.access_token }))
      navigate('/')
    } catch (err) {
      const apiErr = err as ApiError
      setError(apiErr.detail ?? 'Registration failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-soft-cream">
      <header className="border-b border-soft-sage/30 bg-soft-sand/60 py-3">
        <div className="max-w-5xl mx-auto px-4 flex justify-between items-center">
          <Link to="/" className="font-semibold text-soft-navy">AI Video Violence Detection</Link>
          <Link to="/login" className="text-sm text-soft-slate hover:text-soft-navy">Log in</Link>
        </div>
      </header>
      <main id="main-content" className="max-w-md mx-auto mt-12 px-4">
        <div className="rounded-xl border border-soft-sage/40 bg-white/60 p-8 shadow-sm">
        <h1 className="text-2xl font-semibold text-soft-navy mb-6">Register</h1>
        <form onSubmit={handleSubmit} className="space-y-4" aria-label="Register form">
          <div>
            <label htmlFor="reg-username" className="block text-sm font-medium text-soft-slate mb-1">
              Username
            </label>
            <input
              id="reg-username"
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
              minLength={3}
              autoComplete="username"
              aria-required="true"
              aria-describedby={error ? 'register-error' : undefined}
              className="w-full px-3 py-2 rounded-lg border border-soft-sage/50 bg-white focus:ring-2 focus:ring-soft-sage/50 focus:border-soft-sage"
            />
          </div>
          <div>
            <label htmlFor="reg-email" className="block text-sm font-medium text-soft-slate mb-1">
              Email
            </label>
            <input
              id="reg-email"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              autoComplete="email"
              aria-required="true"
              aria-describedby={error ? 'register-error' : undefined}
              className="w-full px-3 py-2 rounded-lg border border-soft-sage/50 bg-white focus:ring-2 focus:ring-soft-sage/50 focus:border-soft-sage"
            />
          </div>
          <div>
            <label htmlFor="reg-password" className="block text-sm font-medium text-soft-slate mb-1">
              Password
            </label>
            <input
              id="reg-password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              minLength={8}
              autoComplete="new-password"
              aria-required="true"
              aria-describedby={error ? 'register-error' : undefined}
              className="w-full px-3 py-2 rounded-lg border border-soft-sage/50 bg-white focus:ring-2 focus:ring-soft-sage/50 focus:border-soft-sage"
            />
          </div>
          {error && (
            <div id="register-error" role="alert" aria-live="assertive" className="text-sm text-red-600">
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
                <span className="sr-only">Creating account, please wait</span>
                <span aria-hidden="true">Creating account…</span>
              </>
            ) : (
              'Create account'
            )}
          </button>
        </form>
        <p className="mt-4 text-sm text-soft-slate">
          Already have an account?{' '}
          <Link to="/login" className="text-soft-navy font-medium hover:underline">
            Login
          </Link>
        </p>
        </div>
      </main>
    </div>
  )
}
