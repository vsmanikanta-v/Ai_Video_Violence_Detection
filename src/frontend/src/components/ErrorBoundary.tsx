import { Component, type ErrorInfo, type ReactNode } from 'react'

interface Props {
  children: ReactNode
}

interface State {
  hasError: boolean
  error: Error | null
}

export class ErrorBoundary extends Component<Props, State> {
  state: State = { hasError: false, error: null }

  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error }
  }

  componentDidCatch(error: Error, info: ErrorInfo) {
    console.error('[ErrorBoundary]', error, info)
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="min-h-screen bg-soft-cream flex items-center justify-center px-4">
          <div className="bg-white/90 rounded-2xl border border-soft-sage/40 shadow-xl p-8 max-w-md w-full text-center">
            <h1 className="text-xl font-bold text-soft-navy mb-2">Something went wrong</h1>
            <p className="text-soft-slate text-sm mb-6">
              An unexpected error occurred. You can try refreshing the page or going back.
            </p>
            {import.meta.env.DEV && this.state.error && (
              <pre className="text-left text-xs bg-red-50 border border-red-200 rounded-lg p-4 mb-6 overflow-auto text-red-700">
                {this.state.error.message}
              </pre>
            )}
            <div className="flex gap-3 justify-center">
              <button
                type="button"
                onClick={() => window.location.reload()}
                className="px-4 py-2 rounded-lg bg-soft-sage/70 text-soft-navy text-sm font-semibold hover:bg-soft-sage transition"
              >
                Refresh page
              </button>
              <button
                type="button"
                onClick={() => window.history.back()}
                className="px-4 py-2 rounded-lg border border-soft-sage/60 text-soft-navy text-sm font-semibold hover:bg-soft-sage/20 transition"
              >
                Go back
              </button>
            </div>
            <p className="mt-6 text-xs text-soft-slate">
              If the problem persists, please contact support.
            </p>
          </div>
        </div>
      )
    }
    return this.props.children
  }
}
