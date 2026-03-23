/**
 * Lightweight API client behavior tests (mocked fetch).
 */
import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest'
import { apiLogin, apiPost, type ApiError } from './client'

describe('API client', () => {
  beforeEach(() => {
    vi.stubGlobal('fetch', vi.fn())
    localStorage.clear()
  })

  afterEach(() => {
    vi.unstubAllGlobals()
  })

  it('apiLogin POSTs to /api/auth/login with JSON body', async () => {
    const mockRes = {
      ok: true,
      text: () => Promise.resolve(JSON.stringify({
        user: { id: 1, username: 'u', email: 'u@x.com', role: 'USER', created_at: '' },
        access_token: 'tok',
        token_type: 'bearer',
      })),
    }
    vi.mocked(fetch).mockResolvedValueOnce(mockRes as unknown as Response)

    const out = await apiLogin({ username: 'u', password: 'p' })

    expect(fetch).toHaveBeenCalledWith(
      expect.stringContaining('/api/auth/login'),
      expect.objectContaining({
        method: 'POST',
        body: JSON.stringify({ username: 'u', password: 'p' }),
      })
    )
    expect(out.access_token).toBe('tok')
    expect(out.user.username).toBe('u')
  })

  it('apiPost throws ApiError when response is not ok', async () => {
    vi.mocked(fetch).mockResolvedValueOnce({
      ok: false,
      status: 401,
      statusText: 'Unauthorized',
      text: () => Promise.resolve(JSON.stringify({ detail: 'Invalid credentials' })),
    } as unknown as Response)

    await expect(apiPost<unknown>('/api/auth/login', {})).rejects.toMatchObject({
      status: 401,
      detail: 'Invalid credentials',
    } as ApiError)
  })
})
