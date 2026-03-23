import type { ResultOut, VideoOut, VideoWithResults } from '@/types'
import { createSlice } from '@reduxjs/toolkit'
import type { PayloadAction } from '@reduxjs/toolkit'

interface VideosState {
  history: VideoWithResults[]
  currentResult: ResultOut | null
  uploadProgress: number | null
  error: string | null
}

const initialState: VideosState = {
  history: [],
  currentResult: null,
  uploadProgress: null,
  error: null,
}

const videosSlice = createSlice({
  name: 'videos',
  initialState,
  reducers: {
    setHistory(state, action: PayloadAction<VideoWithResults[]>) {
      state.history = action.payload
    },
    setCurrentResult(state, action: PayloadAction<ResultOut | null>) {
      state.currentResult = action.payload
    },
    setUploadProgress(state, action: PayloadAction<number | null>) {
      state.uploadProgress = action.payload
    },
    setError(state, action: PayloadAction<string | null>) {
      state.error = action.payload
    },
    addVideoToHistory(state, action: PayloadAction<VideoOut>) {
      const existing = state.history.find((h) => h.video.id === action.payload.id)
      if (!existing) {
        state.history.unshift({ video: action.payload, results: [] })
      }
    },
    addResultToHistory(state, action: PayloadAction<{ videoId: number; result: ResultOut }>) {
      const item = state.history.find((h) => h.video.id === action.payload.videoId)
      if (item) {
        item.results.unshift(action.payload.result)
      }
    },
  },
})

export const {
  setHistory,
  setCurrentResult,
  setUploadProgress,
  setError,
  addVideoToHistory,
  addResultToHistory,
} = videosSlice.actions
export default videosSlice.reducer
