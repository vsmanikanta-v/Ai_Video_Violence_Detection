/**
 * Unit tests for videosSlice reducer and actions.
 * Verifies state transitions for all six video slice actions.
 */
import { describe, it, expect } from 'vitest'
import videosReducer, {
  setHistory,
  setCurrentResult,
  setUploadProgress,
  setError,
  addVideoToHistory,
  addResultToHistory,
} from './videosSlice'
import type { ResultOut, VideoOut, VideoWithResults } from '@/types'

const mockVideo: VideoOut = {
  id: 1,
  user_id: 1,
  filename: 'test.mp4',
  file_size: 1024,
  duration_seconds: 10,
  video_format: 'mp4',
  uploaded_at: '2026-03-15T10:00:00',
}

const mockResult: ResultOut = {
  id: 1,
  video_id: 1,
  violence_score: 0.9,
  prediction: 'VIOLENT',
  confidence_level: 'HIGH',
  key_frame_timestamps: [1, 2, 3],
  processing_time_seconds: 1.5,
  genai_summary: 'Violence detected.',
  created_at: '2026-03-15T10:00:00',
}

describe('videosSlice', () => {
  it('has correct initial state', () => {
    const state = videosReducer(undefined, { type: 'unknown' })
    expect(state.history).toEqual([])
    expect(state.currentResult).toBeNull()
    expect(state.uploadProgress).toBeNull()
    expect(state.error).toBeNull()
  })

  it('setHistory replaces entire history', () => {
    const entry: VideoWithResults = { video: mockVideo, results: [mockResult] }
    const state = videosReducer(undefined, setHistory([entry]))
    expect(state.history).toHaveLength(1)
    expect(state.history[0].video.id).toBe(1)
  })

  it('setCurrentResult stores a result', () => {
    const state = videosReducer(undefined, setCurrentResult(mockResult))
    expect(state.currentResult).toEqual(mockResult)
  })

  it('setCurrentResult clears when given null', () => {
    let state = videosReducer(undefined, setCurrentResult(mockResult))
    state = videosReducer(state, setCurrentResult(null))
    expect(state.currentResult).toBeNull()
  })

  it('setUploadProgress stores progress value', () => {
    const state = videosReducer(undefined, setUploadProgress(42))
    expect(state.uploadProgress).toBe(42)
  })

  it('setError stores error message', () => {
    const state = videosReducer(undefined, setError('Upload failed'))
    expect(state.error).toBe('Upload failed')
  })

  it('addVideoToHistory prepends a new video with empty results', () => {
    const state = videosReducer(undefined, addVideoToHistory(mockVideo))
    expect(state.history).toHaveLength(1)
    expect(state.history[0].video).toEqual(mockVideo)
    expect(state.history[0].results).toEqual([])
  })

  it('addVideoToHistory ignores a video id already in history', () => {
    let state = videosReducer(undefined, addVideoToHistory(mockVideo))
    state = videosReducer(state, addVideoToHistory({ ...mockVideo, filename: 'duplicate.mp4' }))
    expect(state.history).toHaveLength(1)
    expect(state.history[0].video.filename).toBe('test.mp4')
  })

  it('addResultToHistory prepends result to matching video', () => {
    let state = videosReducer(undefined, addVideoToHistory(mockVideo))
    state = videosReducer(state, addResultToHistory({ videoId: 1, result: mockResult }))
    expect(state.history[0].results).toHaveLength(1)
    expect(state.history[0].results[0].id).toBe(1)
  })

  it('addResultToHistory is a no-op for an unknown videoId', () => {
    let state = videosReducer(undefined, addVideoToHistory(mockVideo))
    state = videosReducer(state, addResultToHistory({ videoId: 999, result: mockResult }))
    expect(state.history[0].results).toHaveLength(0)
  })
})
