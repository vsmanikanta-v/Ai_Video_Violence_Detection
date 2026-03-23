/**
 * Lightweight tests for auth slice (reducer and actions).
 * Verifies auth state updates and localStorage sync.
 */
import { describe, it, expect, beforeEach } from 'vitest'
import authReducer, { setAuth, setUser, clearAuth, setLoaded } from './authSlice'
import type { User } from '@/types'

const mockUser: User = {
  id: 1,
  username: 'testuser',
  email: 'test@example.com',
  role: 'USER',
  created_at: '2026-03-14T12:00:00',
}

describe('authSlice', () => {
  beforeEach(() => {
    localStorage.clear()
  })

  it('has initial state with no user and no token', () => {
    const state = authReducer(undefined, { type: 'unknown' })
    expect(state.user).toBeNull()
    expect(state.token).toBeNull()
    expect(state.loaded).toBe(false)
  })

  it('setAuth updates user, token and stores token in localStorage', () => {
    const token = 'jwt-token-123'
    const state = authReducer(undefined, setAuth({ user: mockUser, token }))
    expect(state.user).toEqual(mockUser)
    expect(state.token).toBe(token)
    expect(localStorage.getItem('access_token')).toBe(token)
  })

  it('setUser updates only user', () => {
    const prev = authReducer(undefined, setAuth({ user: mockUser, token: 't' }))
    const updated = authReducer(prev, setUser({ ...mockUser, username: 'other' }))
    expect(updated.user?.username).toBe('other')
    expect(updated.token).toBe('t')
  })

  it('clearAuth clears user, token and removes from localStorage', () => {
    let state = authReducer(undefined, setAuth({ user: mockUser, token: 't' }))
    expect(state.token).toBe('t')
    state = authReducer(state, clearAuth())
    expect(state.user).toBeNull()
    expect(state.token).toBeNull()
    expect(localStorage.getItem('access_token')).toBeNull()
  })

  it('setLoaded updates loaded flag', () => {
    const state = authReducer(undefined, setLoaded(true))
    expect(state.loaded).toBe(true)
  })
})
