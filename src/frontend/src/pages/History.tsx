import { useEffect, useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { apiHistory } from '@/api/client'
import { useAppDispatch, useAppSelector } from '@/store/hooks'
import { setCurrentResult, setError, setHistory } from '@/store/videosSlice'
import type { ResultOut } from '@/types'

export function History() {
  const dispatch = useAppDispatch()
  const navigate = useNavigate()
  const { history, error } = useAppSelector((s) => s.videos)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    let cancelled = false
    dispatch(setError(null))
    apiHistory()
      .then((data) => {
        if (!cancelled) dispatch(setHistory(data))
      })
      .catch(() => {
        if (!cancelled) dispatch(setError('Failed to load history'))
      })
      .finally(() => {
        if (!cancelled) setLoading(false)
      })
    return () => {
      cancelled = true
    }
  }, [dispatch])

  if (loading) {
    return (
      <div className="space-y-6">
        <h1 className="text-2xl font-semibold text-soft-navy">Analysis history</h1>
        <div className="flex justify-center py-12">
          <div className="inline-block h-8 w-8 animate-spin rounded-full border-2 border-soft-sage border-t-transparent" aria-hidden />
          <span className="sr-only">Loading history</span>
        </div>
      </div>
    )
  }

  if (history.length === 0) {
    return (
      <div className="space-y-6">
        <h1 className="text-2xl font-semibold text-soft-navy">Analysis history</h1>
        {error && (
          <div
            className="rounded-lg bg-red-50 border border-red-200 px-4 py-2 text-sm text-red-700"
            role="alert"
            aria-live="assertive"
          >
            {error}
          </div>
        )}
        <div className="rounded-xl border border-soft-sage/40 bg-white/60 p-8 shadow-sm text-center text-soft-slate">
          <p>No videos yet. Upload a video from the home page to get started.</p>
          <Link to="/upload" className="mt-4 inline-block text-soft-navy font-medium hover:underline">
            Go to upload
          </Link>
        </div>
      </div>
    )
  }

  const openResult = (r: ResultOut) => {
    dispatch(setCurrentResult(r))
    navigate(`/results?id=${r.id}`)
  }

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-semibold text-soft-navy">Analysis history</h1>
      {error && (
        <div
          className="rounded-lg bg-red-50 border border-red-200 px-4 py-2 text-sm text-red-700"
          role="alert"
          aria-live="assertive"
        >
          {error}
        </div>
      )}
      <ul className="space-y-4" role="list">
        {history.map((item) => (
          <li
            key={item.video.id}
            className="rounded-xl border border-soft-sage/40 bg-white/60 p-4 shadow-sm"
          >
            <div className="flex flex-wrap items-center justify-between gap-2">
              <p className="font-medium text-soft-navy">{item.video.filename}</p>
              <p className="text-sm text-soft-slate">
                Uploaded {new Date(item.video.uploaded_at).toLocaleString()}
              </p>
            </div>
            {item.results.length > 0 ? (
              <ul className="mt-3 space-y-2 pl-2 border-l-2 border-soft-sage/40" role="list">
                {item.results.map((r) => (
                  <li key={r.id} className="text-sm">
                    <button
                      type="button"
                      onClick={() => openResult(r)}
                      className="text-left w-full rounded p-2 -m-2 hover:bg-soft-sage/20 focus:bg-soft-sage/20 focus:outline-none focus:ring-2 focus:ring-soft-sage"
                      aria-label={`View full result: ${r.prediction}, ${r.confidence_level}, ${(r.violence_score * 100).toFixed(0)}%`}
                    >
                      <span className="font-medium">{r.prediction}</span> ({r.confidence_level},{' '}
                      {(r.violence_score * 100).toFixed(0)}%) —{' '}
                      {new Date(r.created_at).toLocaleString()}
                      {r.genai_summary?.trim() && (
                        <p className="mt-1 text-soft-slate line-clamp-2">{r.genai_summary}</p>
                      )}
                      <span className="mt-1 block text-soft-sage font-medium text-xs">
                        View full result & explanation →
                      </span>
                    </button>
                  </li>
                ))}
              </ul>
            ) : (
              <p className="mt-2 text-sm text-soft-slate">No analysis yet.</p>
            )}
          </li>
        ))}
      </ul>
    </div>
  )
}
