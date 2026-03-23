import type { User } from '@/types'
import { createSlice } from '@reduxjs/toolkit'
import type { PayloadAction } from '@reduxjs/toolkit'

interface AuthState {
  user: User | null
  token: string | null
  loaded: boolean
}

const token = localStorage.getItem('access_token')

const initialState: AuthState = {
  user: null,
  token,
  loaded: false,
}

const authSlice = createSlice({
  name: 'auth',
  initialState,
  reducers: {
    setAuth(state, action: PayloadAction<{ user: User; token: string }>) {
      state.user = action.payload.user
      state.token = action.payload.token
      localStorage.setItem('access_token', action.payload.token)
    },
    setUser(state, action: PayloadAction<User>) {
      state.user = action.payload
    },
    clearAuth(state) {
      state.user = null
      state.token = null
      localStorage.removeItem('access_token')
    },
    setLoaded(state, action: PayloadAction<boolean>) {
      state.loaded = action.payload
    },
  },
})

export const { setAuth, setUser, clearAuth, setLoaded } = authSlice.actions
export default authSlice.reducer
