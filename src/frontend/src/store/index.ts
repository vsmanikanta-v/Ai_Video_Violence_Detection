import { configureStore } from '@reduxjs/toolkit'
import authReducer from './authSlice'
import videosReducer from './videosSlice'

export const store = configureStore({
  reducer: {
    auth: authReducer,
    videos: videosReducer,
  },
})

export type RootState = ReturnType<typeof store.getState>
export type AppDispatch = typeof store.dispatch
