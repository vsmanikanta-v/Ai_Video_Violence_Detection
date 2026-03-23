import { afterEach, describe, it, expect, beforeEach } from 'vitest'
import { render, screen, cleanup } from '@testing-library/react'
import { MemoryRouter, Routes, Route } from 'react-router-dom'
import { Provider } from 'react-redux'
import { configureStore } from '@reduxjs/toolkit'
import authReducer from '@/store/authSlice'
import videosReducer from '@/store/videosSlice'
import { PrivateRoute } from './PrivateRoute'

afterEach(cleanup)

function makeStore(token: string | null) {
  return configureStore({
    reducer: { auth: authReducer, videos: videosReducer },
    preloadedState: { auth: { user: null, token, loaded: true } },
  })
}

describe('PrivateRoute', () => {
  beforeEach(() => {
    localStorage.clear()
  })

  it('renders children when a token is present', () => {
    render(
      <Provider store={makeStore('valid-jwt')}>
        <MemoryRouter>
          <PrivateRoute>
            <span>Protected content</span>
          </PrivateRoute>
        </MemoryRouter>
      </Provider>,
    )
    expect(screen.getByText('Protected content')).toBeTruthy()
  })

  it('redirects to /login and does not render children when token is null', () => {
    render(
      <Provider store={makeStore(null)}>
        <MemoryRouter initialEntries={['/protected']}>
          <Routes>
            <Route
              path="/protected"
              element={
                <PrivateRoute>
                  <span>Protected content</span>
                </PrivateRoute>
              }
            />
            <Route path="/login" element={<span>Login page</span>} />
          </Routes>
        </MemoryRouter>
      </Provider>,
    )
    expect(screen.queryByText('Protected content')).toBeNull()
    expect(screen.getByText('Login page')).toBeTruthy()
  })
})
