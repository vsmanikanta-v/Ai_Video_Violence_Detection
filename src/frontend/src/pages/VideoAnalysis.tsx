import { useEffect, useMemo, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { apiAnalyzeVideo, type ApiError } from '@/api/client'
import { useAppDispatch, useAppSelector } from '@/store/hooks'
import { addResultToHistory, setCurrentResult, setError } from '@/store/videosSlice'
import { VideoUpload } from '@/components/VideoUpload'

export function VideoAnalysis() {
  const dispatch = useAppDispatch()
  const navigate = useNavigate()
  const { error } = useAppSelector((s) => s.videos)
  const [analyzingId, setAnalyzingId] = useState<number | null>(null)
  const [elapsedSeconds, setElapsedSeconds] = useState(0)

  useEffect(() => {
    if (analyzingId === null) {
      setElapsedSeconds(0)
      return
    }

    const startedAt = Date.now()
    const timer = setInterval(() => {
      setElapsedSeconds(Math.floor((Date.now() - startedAt) / 1000))
    }, 1000)

    return () => {
      clearInterval(timer)
    }
  }, [analyzingId])

  const phase = useMemo<'uploaded' | 'ml' | 'genai'>(() => {
    if (elapsedSeconds < 2) return 'uploaded'
    if (elapsedSeconds < 12) return 'ml'
    return 'genai'
  }, [elapsedSeconds])

  const currentStep = useMemo(() => {
    if (phase === 'uploaded') return 1
    if (phase === 'ml') return 2
    return 3
  }, [phase])

  const steps = [
    'Upload complete',
    'ML analysis',
    'GenAI explanation',
  ]

  const handleUploaded = async (videoId: number) => {
    setAnalyzingId(videoId)
    dispatch(setError(null))
    try {
      const res = await apiAnalyzeVideo(videoId)
      dispatch(setCurrentResult(res.result))
      dispatch(addResultToHistory({ videoId, result: res.result }))
      navigate(`/results?id=${res.result.id}`)
    } catch (e) {
      const err = e as ApiError
      dispatch(setError(err.detail ?? 'Analysis failed'))
    } finally {
      setAnalyzingId(null)
    }
  }

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-semibold text-soft-navy">Video upload & analysis</h1>
      <VideoUpload onUploaded={handleUploaded} disabled={analyzingId !== null} />
      {error && (
        <div className="rounded-lg bg-red-50 border border-red-200 px-4 py-2 text-sm text-red-700" role="alert" aria-live="assertive">
          {error}
        </div>
      )}
      {analyzingId !== null && (
        <div
          role="status"
          aria-live="polite"
          aria-label="Analysis in progress"
          className="rounded-xl border border-soft-sage/40 bg-white/60 p-4 shadow-sm"
        >
          <p className="text-sm text-soft-slate">Step {currentStep} of 3</p>
          <ol className="mt-3 grid gap-2 sm:grid-cols-3" aria-label="Processing steps">
            {steps.map((label, index) => {
              const stepNumber = index + 1
              const completed = stepNumber < currentStep
              const active = stepNumber === currentStep

              return (
                <li
                  key={label}
                  className={`rounded-lg border px-3 py-2 text-sm ${
                    active
                      ? 'border-soft-sage bg-soft-sage/20 text-soft-navy'
                      : completed
                        ? 'border-soft-sage/50 bg-soft-sage/10 text-soft-slate'
                        : 'border-soft-sage/30 bg-white/60 text-soft-slate'
                  }`}
                >
                  <span className="inline-flex h-5 w-5 items-center justify-center rounded-full bg-soft-sand text-xs font-semibold text-soft-navy">
                    {completed ? '✓' : stepNumber}
                  </span>
                  <span className="ml-2">{label}</span>
                </li>
              )
            })}
          </ol>
          <p className="mt-1 font-medium text-soft-navy">
            {phase === 'uploaded' && 'Video uploaded successfully. Preparing analysis...'}
            {phase === 'ml' && 'Analyzing video frames for violence patterns...'}
            {phase === 'genai' && 'Generating incident explanation...'}
          </p>
          <p className="mt-1 text-sm text-soft-slate">Processing for {elapsedSeconds}s</p>
          {elapsedSeconds >= 15 && (
            <p className="mt-2 text-sm text-soft-slate">This is taking longer than usual, but processing is still active.</p>
          )}
        </div>
      )}
    </div>
  )
}
