import { useEffect } from 'react'
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { apiMe } from '@/api/client'
import { useAppDispatch, useAppSelector } from '@/store/hooks'
import { clearAuth, setLoaded, setUser } from '@/store/authSlice'
import { Layout } from '@/components/Layout'
import { PrivateRoute } from '@/components/PrivateRoute'
import { AdminRoute } from '@/components/AdminRoute'
import { SkipNavigation } from '@/components/SkipNavigation'
import { ErrorBoundary } from '@/components/ErrorBoundary'
import { Login } from '@/pages/Login'
import { Register } from '@/pages/Register'
import { LandingPage } from '@/pages/LandingPage'
import { VideoAnalysis } from '@/pages/VideoAnalysis'
import { DetectionResults } from '@/pages/DetectionResults'
import { History } from '@/pages/History'
import { AdminDashboard } from '@/pages/AdminDashboard'

function AppRoutes() {
  const { token, user, loaded } = useAppSelector((s) => s.auth)
  const dispatch = useAppDispatch()

  useEffect(() => {
    if (!token) {
      dispatch(setLoaded(true))
      return
    }
    // User already set (e.g. from login response) — skip redundant /me call
    if (user) {
      dispatch(setLoaded(true))
      return
    }
    const controller = new AbortController()
    apiMe(controller.signal)
      .then((data) => {
        if (!controller.signal.aborted) dispatch(setUser(data.user))
      })
      .catch(() => {
        if (!controller.signal.aborted) dispatch(clearAuth())
      })
      .finally(() => {
        if (!controller.signal.aborted) dispatch(setLoaded(true))
      })
    return () => controller.abort()
  }, [token, user, dispatch])

  if (!loaded) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-soft-cream">
        <div className="text-center">
          <div className="inline-block h-10 w-10 animate-spin rounded-full border-2 border-soft-sage border-t-transparent" aria-hidden />
          <p className="mt-4 text-soft-slate">Loading…</p>
        </div>
      </div>
    )
  }

  return (
    <Routes>
      <Route path="/" element={<LandingPage />} />
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />
      <Route element={<Layout />}>
        <Route path="upload" element={<PrivateRoute><VideoAnalysis /></PrivateRoute>} />
        <Route path="results" element={<PrivateRoute><DetectionResults /></PrivateRoute>} />
        <Route path="history" element={<PrivateRoute><History /></PrivateRoute>} />
        <Route path="admin" element={<AdminRoute><AdminDashboard /></AdminRoute>} />
      </Route>
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  )
}

export default function App() {
  return (
    <ErrorBoundary>
      <BrowserRouter>
        <SkipNavigation />
        <AppRoutes />
      </BrowserRouter>
    </ErrorBoundary>
  )
}
