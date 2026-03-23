import { useCallback, useState } from 'react'
import { apiUploadVideo, type ApiError } from '@/api/client'
import { useAppDispatch, useAppSelector } from '@/store/hooks'
import { addVideoToHistory, setError, setUploadProgress } from '@/store/videosSlice'

const ALLOWED = ['.mp4', '.avi', '.webm', '.mov', '.mkv']
const MAX_MB = 2

interface VideoUploadProps {
  onUploaded?: (videoId: number) => void
}

export function VideoUpload({ onUploaded }: VideoUploadProps) {
  const dispatch = useAppDispatch()
  const progress = useAppSelector((s) => s.videos.uploadProgress)
  const [file, setFile] = useState<File | null>(null)
  const [validationError, setValidationError] = useState<string | null>(null)

  const validate = useCallback((f: File): string | null => {
    const ext = '.' + f.name.split('.').pop()?.toLowerCase()
    if (!ALLOWED.includes(ext)) {
      return `Allowed formats: ${ALLOWED.join(', ')}`
    }
    if (f.size > MAX_MB * 1024 * 1024) {
      return `Max file size: ${MAX_MB} MB`
    }
    return null
  }, [])

  const onFileChange = useCallback(
    (e: React.ChangeEvent<HTMLInputElement>) => {
      const f = e.target.files?.[0]
      if (!f) {
        setFile(null)
        setValidationError(null)
        return
      }
      const err = validate(f)
      setValidationError(err)
      setFile(err ? null : f)
    },
    [validate]
  )

  const upload = useCallback(async () => {
    if (!file) return
    dispatch(setError(null))
    dispatch(setUploadProgress(0))
    try {
      const res = await apiUploadVideo(file, (p) => dispatch(setUploadProgress(p.percent)))
      dispatch(addVideoToHistory(res.video))
      dispatch(setUploadProgress(100))
      setTimeout(() => dispatch(setUploadProgress(null)), 800)
      setFile(null)
      setValidationError(null)
      onUploaded?.(res.video.id)
    } catch (e) {
      const err = e as ApiError
      dispatch(setError(err.detail ?? 'Upload failed'))
      dispatch(setUploadProgress(null))
    }
  }, [file, dispatch, onUploaded])

  return (
    <div className="rounded-xl border border-soft-sage/40 bg-white/60 p-6 shadow-sm">
      <h2 className="text-lg font-semibold text-soft-navy mb-4">Upload video</h2>
      <div className="flex flex-col sm:flex-row gap-4 items-start">
        <div className="flex-1 w-full">
          <label htmlFor="video-file-input" className="sr-only">
            Video file upload
          </label>
          <input
            id="video-file-input"
            type="file"
            accept={ALLOWED.join(',')}
            onChange={onFileChange}
            aria-describedby="video-upload-help"
            className="block w-full text-sm text-soft-slate file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:bg-soft-sage/30 file:text-soft-navy"
          />
          <p id="video-upload-help" className="mt-1 text-xs text-soft-slate">
            Select a video file (MP4, AVI, WebM, MOV, MKV). Max {MAX_MB} MB.
          </p>
        </div>
        <button
          type="button"
          onClick={upload}
          disabled={!file || progress !== null}
          aria-busy={progress !== null && progress < 100}
          className="px-4 py-2 rounded-lg bg-soft-sage/50 text-soft-navy font-medium hover:bg-soft-sage/70 disabled:opacity-50 disabled:cursor-not-allowed transition"
        >
          {progress !== null && progress < 100 ? (
            <>
              <span className="sr-only">Uploading, please wait</span>
              <span aria-hidden="true">Uploading {progress}%</span>
            </>
          ) : (
            'Upload'
          )}
        </button>
      </div>
      {validationError && (
        <p className="mt-2 text-sm text-red-600" role="alert" aria-live="assertive">
          {validationError}
        </p>
      )}
      {progress !== null && progress < 100 && (
        <div
          className="mt-4 h-2 rounded-full bg-soft-sand overflow-hidden"
          role="progressbar"
          aria-valuenow={progress}
          aria-valuemin={0}
          aria-valuemax={100}
          aria-label={`Upload progress ${progress}%`}
        >
          <div
            className="h-full bg-soft-sage transition-all duration-300"
            style={{ width: `${progress}%` }}
            aria-hidden
          />
        </div>
      )}
    </div>
  )
}
