import { useEffect, useState } from 'react'
import { Link, useSearchParams } from 'react-router-dom'
import { apiGetDetectionByResultId } from '@/api/client'
import { useAppSelector } from '@/store/hooks'
import type { ResultOut } from '@/types'

export function DetectionResults() {
  const reduxResult = useAppSelector((s) => s.videos.currentResult)
  const [searchParams] = useSearchParams()
  const resultIdParam = searchParams.get('id')
  const [fetchedResult, setFetchedResult] = useState<ResultOut | null>(null)
  const [loading, setLoading] = useState(false)
  const [fetchError, setFetchError] = useState<string | null>(null)

  useEffect(() => {
    if (reduxResult || !resultIdParam) return
    let cancelled = false
    setLoading(true)
    setFetchError(null)
    const numericId = Number(resultIdParam)
    if (Number.isNaN(numericId) || numericId <= 0) {
      setFetchError('Invalid result ID')
      setLoading(false)
      return
    }
    apiGetDetectionByResultId(numericId)
      .then((data) => {
        if (!cancelled) setFetchedResult(data)
      })
      .catch(() => {
        if (!cancelled) setFetchError('Could not load detection result')
      })
      .finally(() => {
        if (!cancelled) setLoading(false)
      })
    return () => {
      cancelled = true
    }
  }, [reduxResult, resultIdParam])

  const result = reduxResult ?? fetchedResult

  if (loading) {
    return (
      <div className="space-y-6">
        <h1 className="text-2xl font-semibold text-soft-navy">Detection result</h1>
        <div className="flex justify-center py-12">
          <div className="inline-block h-8 w-8 animate-spin rounded-full border-2 border-soft-sage border-t-transparent" aria-hidden />
          <span className="sr-only">Loading result</span>
        </div>
      </div>
    )
  }

  if (fetchError) {
    return (
      <div className="space-y-6">
        <h1 className="text-2xl font-semibold text-soft-navy">Detection result</h1>
        <div className="rounded-lg bg-red-50 border border-red-200 px-4 py-2 text-sm text-red-700" role="alert">
          {fetchError}
        </div>
        <p className="text-sm text-soft-slate">
          <Link to="/history" className="text-soft-sage hover:text-soft-navy font-medium focus:outline-none focus:ring-2 focus:ring-soft-sage rounded">
            View history
          </Link>
        </p>
      </div>
    )
  }

  if (!result) {
    return (
      <div className="space-y-6">
        <h1 className="text-2xl font-semibold text-soft-navy">Detection result</h1>
        <div className="rounded-xl border border-soft-sage/40 bg-white/60 p-8 shadow-sm text-center text-soft-slate">
          <p>No detection result to show. Upload a video and run analysis to see results here.</p>
          <Link to="/upload" className="mt-4 inline-block text-soft-sage font-medium hover:text-soft-navy focus:outline-none focus:ring-2 focus:ring-soft-sage rounded">
            Go to upload
          </Link>
        </div>
      </div>
    )
  }

  const isViolent = result.prediction === 'VIOLENT'
  const confidenceColor =
    result.confidence_level === 'HIGH'
      ? 'text-red-700'
      : result.confidence_level === 'MEDIUM'
        ? 'text-amber-700'
        : 'text-soft-slate'

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-semibold text-soft-navy">Detection result</h1>
      <section
        className="rounded-xl border border-soft-sage/40 bg-white/60 p-6 shadow-sm space-y-4"
        aria-label="Detection results and incident explanation"
      >
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div>
            <p className="text-sm font-medium text-soft-slate">Prediction</p>
            <p className={`font-semibold ${isViolent ? 'text-red-600' : 'text-green-700'}`}>
              {result.prediction}
            </p>
          </div>
          <div>
            <p className="text-sm font-medium text-soft-slate">Confidence</p>
            <p className={`font-semibold ${confidenceColor}`}>{result.confidence_level}</p>
          </div>
          <div>
            <p className="text-sm font-medium text-soft-slate">Violence score</p>
            <p className="font-mono">{(result.violence_score * 100).toFixed(1)}%</p>
          </div>
          {result.processing_time_seconds != null && (
            <div>
              <p className="text-sm font-medium text-soft-slate">Processing time</p>
              <p className="font-mono">{result.processing_time_seconds.toFixed(2)}s</p>
            </div>
          )}
        </div>
        {result.key_frame_timestamps.length > 0 && (
          <div>
            <p className="text-sm font-medium text-soft-slate mb-1">Key frame timestamps (s)</p>
            <p className="font-mono text-sm">{result.key_frame_timestamps.join(', ')}</p>
          </div>
        )}
        <div>
          <h2 id="explanation-heading" className="text-sm font-medium text-soft-slate mb-2">
            Incident explanation
          </h2>
          <div
            className="rounded-lg bg-soft-sand/60 p-4 text-soft-navy whitespace-pre-wrap"
            aria-labelledby="explanation-heading"
          >
            {result.genai_summary?.trim()
              ? result.genai_summary
              : 'Explanation not available for this result.'}
          </div>
        </div>
      </section>
      <p className="text-sm text-soft-slate">
        <Link to="/history" className="text-soft-sage hover:text-soft-navy font-medium focus:outline-none focus:ring-2 focus:ring-soft-sage rounded">
          View history
        </Link>
      </p>
    </div>
  )
}
