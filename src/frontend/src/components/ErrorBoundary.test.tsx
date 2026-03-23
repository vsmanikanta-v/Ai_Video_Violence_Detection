import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import { render, screen, cleanup } from '@testing-library/react'
import { ErrorBoundary } from './ErrorBoundary'

function Thrower({ shouldThrow }: { shouldThrow: boolean }) {
  if (shouldThrow) throw new Error('Test error')
  return <span>Child content</span>
}

describe('ErrorBoundary', () => {
  afterEach(cleanup)

  beforeEach(() => {
    vi.spyOn(console, 'error').mockImplementation(() => {})
  })

  it('renders children when there is no error', () => {
    render(
      <ErrorBoundary>
        <Thrower shouldThrow={false} />
      </ErrorBoundary>,
    )
    expect(screen.getByText('Child content')).toBeTruthy()
    expect(screen.queryByText(/Something went wrong/i)).toBeNull()
  })

  it('shows fallback UI when a child throws', () => {
    render(
      <ErrorBoundary>
        <Thrower shouldThrow={true} />
      </ErrorBoundary>,
    )
    expect(screen.getByText(/Something went wrong/i)).toBeTruthy()
    expect(screen.getByText(/An unexpected error occurred/i)).toBeTruthy()
    expect(screen.getByRole('button', { name: /Refresh page/i })).toBeTruthy()
    expect(screen.getByRole('button', { name: /Go back/i })).toBeTruthy()
    expect(screen.getByText(/If the problem persists/i)).toBeTruthy()
  })
})
