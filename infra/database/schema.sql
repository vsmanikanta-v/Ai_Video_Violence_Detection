-- PostgreSQL Schema for AI Video Violence Detection System
-- This schema defines tables for users, videos, detection results, and audit logging

-- Drop existing tables if they exist (development only)
DROP TABLE IF EXISTS audit_logs CASCADE;
DROP TABLE IF EXISTS results CASCADE;
DROP TABLE IF EXISTS videos CASCADE;
DROP TABLE IF EXISTS users CASCADE;

-- ============================================================================
-- Users Table
-- ============================================================================
-- Stores user authentication information and role-based access control
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL DEFAULT 'USER',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for efficient user lookups
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_role ON users(role);

-- ============================================================================
-- Videos Table
-- ============================================================================
-- Stores uploaded video metadata and file information
CREATE TABLE videos (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    file_path TEXT NOT NULL,
    filename VARCHAR(500) NOT NULL,
    file_size BIGINT,
    duration_seconds INTEGER,
    video_format VARCHAR(50),
    uploaded_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
    -- Foreign key constraint with cascade delete
    CONSTRAINT fk_videos_user
        FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE
);

-- Indexes for efficient video queries
CREATE INDEX idx_videos_user_id ON videos(user_id);
CREATE INDEX idx_videos_uploaded_at ON videos(uploaded_at DESC);
CREATE INDEX idx_videos_user_uploaded ON videos(user_id, uploaded_at DESC);

-- ============================================================================
-- Results Table
-- ============================================================================
-- Stores violence detection results and GenAI-generated incident explanations
CREATE TABLE results (
    id SERIAL PRIMARY KEY,
    video_id INTEGER NOT NULL,
    violence_score FLOAT NOT NULL CHECK (violence_score >= 0.0 AND violence_score <= 1.0),
    prediction VARCHAR(50) NOT NULL CHECK (prediction IN ('VIOLENT', 'NON_VIOLENT')),
    confidence_level VARCHAR(50) NOT NULL CHECK (confidence_level IN ('HIGH', 'MEDIUM', 'LOW')),
    key_frame_timestamps INTEGER[],
    processing_time_seconds FLOAT,
    genai_summary TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
    -- Foreign key constraint with cascade delete
    CONSTRAINT fk_results_video
        FOREIGN KEY (video_id)
        REFERENCES videos(id)
        ON DELETE CASCADE
);

-- Indexes for efficient result queries
CREATE INDEX idx_results_video_id ON results(video_id);
CREATE INDEX idx_results_prediction ON results(prediction);
CREATE INDEX idx_results_confidence_level ON results(confidence_level);
CREATE INDEX idx_results_created_at ON results(created_at DESC);
CREATE INDEX idx_results_video_created ON results(video_id, created_at DESC);
CREATE INDEX idx_results_violence_score ON results(violence_score DESC);

-- ============================================================================
-- Audit Logs Table
-- ============================================================================
-- Tracks system actions and events for compliance and traceability
CREATE TABLE audit_logs (
    id SERIAL PRIMARY KEY,
    user_id INTEGER,
    action VARCHAR(100) NOT NULL,
    entity_type VARCHAR(50),
    entity_id INTEGER,
    request_context_id VARCHAR(100),
    details TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
    -- Foreign key constraint with SET NULL on delete
    CONSTRAINT fk_audit_logs_user
        FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE SET NULL
);

-- Indexes for efficient audit log queries
CREATE INDEX idx_audit_logs_user_id ON audit_logs(user_id);
CREATE INDEX idx_audit_logs_created_at ON audit_logs(created_at DESC);
CREATE INDEX idx_audit_logs_user_created ON audit_logs(user_id, created_at DESC);
CREATE INDEX idx_audit_logs_action_created ON audit_logs(action, created_at DESC);
CREATE INDEX idx_audit_logs_request_context ON audit_logs(request_context_id);

-- ============================================================================
-- Comments
-- ============================================================================

-- Users Table:
--   - id: Auto-incrementing primary key
--   - email: Unique email address for registration/contact (login uses `username`, not email)
--   - password_hash: Hashed password (never store plain text)
--   - role: USER or ADMIN for role-based access control
--   - created_at: Timestamp of account creation

-- Videos Table:
--   - id: Auto-incrementing primary key
--   - user_id: Foreign key to users (CASCADE DELETE: when user is deleted, their videos are also deleted)
--   - file_path: Path to stored video file on server
--   - filename: Original filename of uploaded video
--   - file_size: Size of video file in bytes
--   - duration_seconds: Duration of video in seconds
--   - video_format: Video format (MP4, AVI, etc.)
--   - uploaded_at: Timestamp of video upload
--   - Composite index (user_id, uploaded_at) for efficient user video history queries

-- Results Table:
--   - id: Auto-incrementing primary key
--   - video_id: Foreign key to videos (CASCADE DELETE: when video is deleted, results are also deleted)
--   - violence_score: Probability score from CNN-LSTM model (0.0 to 1.0)
--   - prediction: Classification result (VIOLENT or NON_VIOLENT)
--   - confidence_level: Confidence category (HIGH: score>=0.8 or <=0.2; MEDIUM: score>=0.6 or <=0.4; LOW: 0.4<score<0.6)
--   - key_frame_timestamps: Array of timestamps where violence was detected (in seconds)
--   - processing_time_seconds: Time taken for ML inference
--   - genai_summary: Human-readable incident explanation generated by GenAI
--   - created_at: Timestamp of result generation
--   - Multiple indexes for different query patterns (by video, prediction, confidence, score)

-- Audit Logs Table:
--   - id: Auto-incrementing primary key
--   - user_id: Foreign key to users (SET NULL on DELETE: preserve logs even if user is deleted)
--   - action: Action performed (e.g., 'video_uploaded', 'video_analyzed', 'login', 'admin_view')
--   - entity_type: Type of entity affected (e.g., 'video', 'result', 'user')
--   - entity_id: ID of affected entity (optional)
--   - request_context_id: Unique request/session identifier for correlation
--   - details: Additional context as text (optional)
--   - created_at: Timestamp of the action
--   - Multiple indexes for different audit query patterns

-- ============================================================================
-- Access Patterns
-- ============================================================================

-- 1. User Video History (most common query):
--    SELECT * FROM videos WHERE user_id = ? ORDER BY uploaded_at DESC;
--    -> Optimized by idx_videos_user_uploaded

-- 2. Video Detection Results:
--    SELECT * FROM results WHERE video_id = ? ORDER BY created_at DESC;
--    -> Optimized by idx_results_video_created

-- 3. High Confidence Violent Detections (Admin):
--    SELECT * FROM results WHERE prediction = 'VIOLENT' AND confidence_level = 'HIGH' ORDER BY created_at DESC;
--    -> Optimized by idx_results_prediction and idx_results_confidence_level

-- 4. User Audit History:
--    SELECT * FROM audit_logs WHERE user_id = ? ORDER BY created_at DESC;
--    -> Optimized by idx_audit_logs_user_created

-- 5. System-wide Audit Logs:
--    SELECT * FROM audit_logs ORDER BY created_at DESC;
--    -> Optimized by idx_audit_logs_created_at

-- 6. Action-based Audit Query:
--    SELECT * FROM audit_logs WHERE action = ? ORDER BY created_at DESC;
--    -> Optimized by idx_audit_logs_action_created

-- 7. Request Context Correlation:
--    SELECT * FROM audit_logs WHERE request_context_id = ?;
--    -> Optimized by idx_audit_logs_request_context

-- ============================================================================
-- Sample Data (Optional - for testing)
-- ============================================================================

-- Uncomment to insert sample data:
/*
-- Insert sample user (username required by schema)
INSERT INTO users (username, email, password_hash, role)
VALUES ('admin', 'admin@example.com', 'hashed_password_here', 'ADMIN');

-- Insert sample video
INSERT INTO videos (user_id, file_path, filename, duration_seconds, video_format)
VALUES (1, '/uploads/video_001.mp4', 'surveillance_camera_3_20260114.mp4', 45, 'MP4');

-- Insert sample detection result
INSERT INTO results (video_id, violence_score, prediction, confidence_level, key_frame_timestamps, genai_summary)
VALUES (1, 0.87, 'VIOLENT', 'HIGH', ARRAY[12, 18, 25, 32], 'A violent incident was detected with high confidence...');

-- Insert sample audit log
INSERT INTO audit_logs (user_id, action, entity_type, entity_id, request_context_id)
VALUES (1, 'video_uploaded', 'video', 1, 'req-12345');
*/

-- ============================================================================
-- End of Schema
-- ============================================================================
