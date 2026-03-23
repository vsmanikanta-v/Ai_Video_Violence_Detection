import { useState } from 'react'
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
      <VideoUpload onUploaded={handleUploaded} />
      {error && (
        <div className="rounded-lg bg-red-50 border border-red-200 px-4 py-2 text-sm text-red-700" role="alert" aria-live="assertive">
          {error}
        </div>
      )}
      {analyzingId !== null && (
        <div role="status" aria-live="polite" aria-label="Analysis in progress" className="text-soft-slate">
          Running violence detection and generating explanation…
        </div>
      )}
    </div>
  )
}
