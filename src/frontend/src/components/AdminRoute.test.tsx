import { afterEach, describe, it, expect, beforeEach } from 'vitest'
import { render, screen, cleanup } from '@testing-library/react'
import { MemoryRouter, Routes, Route } from 'react-router-dom'
import { Provider } from 'react-redux'
import { configureStore } from '@reduxjs/toolkit'
import authReducer from '@/store/authSlice'
import videosReducer from '@/store/videosSlice'
import { AdminRoute } from './AdminRoute'
import type { User } from '@/types'

afterEach(cleanup)

const adminUser: User = {
  id: 2,
  username: 'adminuser',
  email: 'admin@example.com',
  role: 'ADMIN',
  created_at: '2026-03-15T10:00:00',
}

const regularUser: User = {
  id: 1,
  username: 'testuser',
  email: 'test@example.com',
  role: 'USER',
  created_at: '2026-03-15T10:00:00',
}

function makeStore(token: string | null, user: User | null) {
  return configureStore({
    reducer: { auth: authReducer, videos: videosReducer },
    preloadedState: { auth: { user, token, loaded: true } },
  })
}

describe('AdminRoute', () => {
  beforeEach(() => {
    localStorage.clear()
  })

  it('renders children for an authenticated ADMIN user', () => {
    render(
      <Provider store={makeStore('admin-jwt', adminUser)}>
        <MemoryRouter>
          <AdminRoute>
            <span>Admin content</span>
          </AdminRoute>
        </MemoryRouter>
      </Provider>,
    )
    expect(screen.getByText('Admin content')).toBeTruthy()
  })

  it('redirects to / and does not render children for a USER role', () => {
    render(
      <Provider store={makeStore('user-jwt', regularUser)}>
        <MemoryRouter initialEntries={['/admin']}>
          <Routes>
            <Route
              path="/admin"
              element={
                <AdminRoute>
                  <span>Admin content</span>
                </AdminRoute>
              }
            />
            <Route path="/" element={<span>Home page</span>} />
          </Routes>
        </MemoryRouter>
      </Provider>,
    )
    expect(screen.queryByText('Admin content')).toBeNull()
    expect(screen.getByText('Home page')).toBeTruthy()
  })

  it('redirects to /login and does not render children when no token', () => {
    render(
      <Provider store={makeStore(null, null)}>
        <MemoryRouter initialEntries={['/admin']}>
          <Routes>
            <Route
              path="/admin"
              element={
                <AdminRoute>
                  <span>Admin content</span>
                </AdminRoute>
              }
            />
            <Route path="/login" element={<span>Login page</span>} />
          </Routes>
        </MemoryRouter>
      </Provider>,
    )
    expect(screen.queryByText('Admin content')).toBeNull()
    expect(screen.getByText('Login page')).toBeTruthy()
  })
})
