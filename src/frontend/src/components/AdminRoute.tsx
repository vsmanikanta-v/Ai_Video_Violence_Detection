import type { ReactNode } from 'react'
import { Navigate } from 'react-router-dom'
import { useAppSelector } from '@/store/hooks'

interface AdminRouteProps {
  children: ReactNode
}

export function AdminRoute({ children }: AdminRouteProps) {
  const { token, user } = useAppSelector((s) => s.auth)

  if (!token) {
    return <Navigate to="/login" replace />
  }
  if (user?.role !== 'ADMIN') {
    return <Navigate to="/" replace />
  }
  return <>{children}</>
}
