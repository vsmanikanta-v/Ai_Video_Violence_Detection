export interface User {
  id: number
  username: string
  email: string
  role: 'USER' | 'ADMIN'
  created_at: string
}

export interface VideoOut {
  id: number
  user_id: number
  filename: string
  file_size: number | null
  duration_seconds: number | null
  video_format: string | null
  uploaded_at: string
}

export interface ResultOut {
  id: number
  video_id: number
  violence_score: number
  prediction: 'VIOLENT' | 'NON_VIOLENT'
  confidence_level: 'HIGH' | 'MEDIUM' | 'LOW'
  key_frame_timestamps: number[]
  processing_time_seconds: number | null
  genai_summary: string | null
  created_at: string
  /** Detection status: complete (sync), pending/failed if async added later */
  status?: 'pending' | 'complete' | 'failed'
}

export interface VideoWithResults {
  video: VideoOut
  results: ResultOut[]
}

export interface AuthResponse {
  user: User
  access_token: string
  token_type: string
}

export interface UploadResponse {
  video: VideoOut
  message: string
}

export interface AnalyzeResponse {
  result: ResultOut
  message: string
}

export interface AdminStats {
  total_users: number
  total_videos: number
  total_results: number
  total_audit_logs: number
}

export interface AuditLogEntry {
  id: number
  user_id: number | null
  username: string | null
  action: string
  entity_type: string | null
  entity_id: number | null
  request_context_id: string | null
  details: string | null
  created_at: string | null
}
