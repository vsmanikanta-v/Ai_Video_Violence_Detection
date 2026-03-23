/**
 * API client with base URL, JWT header injection, and error handling.
 * Video upload supports progress callback.
 */

import type {
  AnalyzeResponse,
  AuthResponse,
  ResultOut,
  UploadResponse,
  User,
  VideoOut,
  VideoWithResults,
} from '@/types'

const BASE_URL = import.meta.env.VITE_API_URL ?? ''

function getToken(): string | null {
  return localStorage.getItem('access_token')
}

function getHeaders(omitAuth = false): Record<string, string> {
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
  }
  if (!omitAuth) {
    const token = getToken()
    if (token) headers['Authorization'] = `Bearer ${token}`
  }
  return headers
}

export interface ApiError {
  detail: string
  status: number
}

async function handleResponse<T>(res: Response): Promise<T> {
  const text = await res.text()
  let data: unknown
  try {
    data = text ? JSON.parse(text) : null
  } catch {
    data = { detail: text || res.statusText }
  }
  if (!res.ok) {
    const detail = typeof (data as { detail?: string })?.detail === 'string'
      ? (data as { detail: string }).detail
      : res.statusText
    throw { detail, status: res.status } as ApiError
  }
  return data as T
}

/** Parse XHR response text and either resolve or reject based on status. */
function handleXhrResponse<T>(
  text: string,
  status: number,
  statusText: string,
  resolve: (value: T) => void,
  reject: (reason: ApiError) => void
): void {
  let data: unknown
  try {
    data = text ? JSON.parse(text) : null
  } catch {
    data = { detail: text || statusText }
  }
  if (status >= 200 && status < 300) {
    resolve(data as T)
  } else {
    const detail = typeof (data as { detail?: string })?.detail === 'string'
      ? (data as { detail: string }).detail
      : statusText
    reject({ detail, status } as ApiError)
  }
}

export async function apiGet<T>(path: string): Promise<T> {
  const res = await fetch(`${BASE_URL}${path}`, { headers: getHeaders() })
  return handleResponse<T>(res)
}

export async function apiPost<T>(path: string, body: unknown): Promise<T> {
  const res = await fetch(`${BASE_URL}${path}`, {
    method: 'POST',
    headers: getHeaders(),
    body: JSON.stringify(body),
  })
  return handleResponse<T>(res)
}

export interface UploadProgress {
  loaded: number
  total: number
  percent: number
}

export function apiUploadVideo(
  file: File,
  onProgress?: (p: UploadProgress) => void
): Promise<UploadResponse> {
  const token = getToken()
  const form = new FormData()
  form.append('file', file)

  return new Promise((resolve, reject) => {
    const xhr = new XMLHttpRequest()
    xhr.open('POST', `${BASE_URL}/api/videos/upload`)

    if (token) {
      xhr.setRequestHeader('Authorization', `Bearer ${token}`)
    }

    xhr.upload.addEventListener('progress', (e) => {
      if (e.lengthComputable && onProgress) {
        onProgress({
          loaded: e.loaded,
          total: e.total,
          percent: Math.round((e.loaded / e.total) * 100),
        })
      }
    })

    xhr.addEventListener('load', () => {
      handleXhrResponse<UploadResponse>(xhr.responseText, xhr.status, xhr.statusText, resolve, reject)
    })

    xhr.addEventListener('error', () => {
      reject({ detail: 'Network error', status: 0 } as ApiError)
    })

    xhr.send(form)
  })
}

export async function apiAnalyzeVideo(videoId: number): Promise<AnalyzeResponse> {
  const res = await fetch(`${BASE_URL}/api/videos/${videoId}/analyze`, {
    method: 'POST',
    headers: getHeaders(),
  })
  return handleResponse<AnalyzeResponse>(res)
}

export async function apiHistory(signal?: AbortSignal): Promise<VideoWithResults[]> {
  const res = await fetch(`${BASE_URL}/api/videos/history`, { headers: getHeaders(), signal })
  return handleResponse<VideoWithResults[]>(res)
}

export async function apiGetVideo(videoId: number): Promise<VideoOut> {
  const res = await fetch(`${BASE_URL}/api/videos/${videoId}`, { headers: getHeaders() })
  return handleResponse<VideoOut>(res)
}

/** Fetch a single detection result by id (user must own the video). */
export async function apiGetDetectionByResultId(resultId: number): Promise<ResultOut> {
  const res = await fetch(`${BASE_URL}/api/detections/result/${resultId}`, {
    headers: getHeaders(),
  })
  return handleResponse<ResultOut>(res)
}

/** Fetch all detection results for a video (user must own the video). */
export async function apiGetDetectionsByVideoId(videoId: number): Promise<ResultOut[]> {
  const res = await fetch(`${BASE_URL}/api/detections/video/${videoId}`, {
    headers: getHeaders(),
  })
  return handleResponse<ResultOut[]>(res)
}

// Auth (no token in header for login/register)
export async function apiRegister(body: {
  username: string
  email: string
  password: string
  role?: 'USER'
}): Promise<AuthResponse> {
  const res = await fetch(`${BASE_URL}/api/auth/register`, {
    method: 'POST',
    headers: getHeaders(true),
    body: JSON.stringify(body),
  })
  return handleResponse<AuthResponse>(res)
}

export async function apiLogin(body: { username: string; password: string }): Promise<AuthResponse> {
  const res = await fetch(`${BASE_URL}/api/auth/login`, {
    method: 'POST',
    headers: getHeaders(true),
    body: JSON.stringify(body),
  })
  return handleResponse<AuthResponse>(res)
}

export async function apiMe(signal?: AbortSignal): Promise<{ user: User }> {
  const res = await fetch(`${BASE_URL}/api/auth/me`, { headers: getHeaders(), signal })
  return handleResponse<{ user: User }>(res)
}
