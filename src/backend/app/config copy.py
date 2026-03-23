"""Configuration management for AI Video Violence Detection.

Uses pydantic-settings to load environment variables with validation.
All secrets must be provided via environment variables.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables.

    Attributes:
        jwt_secret_key: Secret key for JWT token signing
        jwt_algorithm: Algorithm for JWT encoding (default: HS256)
        jwt_access_token_expire_minutes: Token expiration time in minutes
        database_url: PostgreSQL connection string
        create_default_users: If True, create default admin/user on startup (dev only)
        default_admin_username: Username for default admin (when create_default_users=True)
        default_admin_password: Password for default admin
        default_admin_email: Email for default admin
        default_user_username: Username for default user
        default_user_password: Password for default user
        default_user_email: Email for default user
        gemini_api_key: Optional; when set, incident explanations use Gemini API
        gemini_model: Gemini model name (default gemini-3-flash-preview)
        upload_dir: Directory for uploaded video files
        max_upload_size_mb: Maximum upload file size in megabytes
        cors_allowed_origins: Allowed CORS origins (list); defaults to React dev servers
    """

    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 30
    database_url: str = "postgresql://postgres:postgres@localhost:5432/ai_video_violence"

    # Default users (development only — do not enable in production)
    create_default_users: bool = False
    default_admin_username: str = "admin"
    default_admin_password: str = ""
    default_admin_email: str = "admin@localhost"
    default_user_username: str = "user"
    default_user_password: str = ""
    default_user_email: str = "user@localhost"

    # GenAI — incident explanation (optional; omit for mock/placeholder)
    gemini_api_key: str | None = None
    gemini_model: str = "gemini-3-flash-preview"

    # Video upload
    upload_dir: str = "uploads"
    max_upload_size_mb: int = 10

    # Rate limiting (per IP; cost control and DoS mitigation)
    ratelimit_enabled: bool = True
    ratelimit_default: str = "50 per hour"
    ratelimit_video_upload: str = "5 per minute"
    ratelimit_video_analysis: str = "10 per minute"

    # CORS — allowed origins for the API (comma-separated; dev defaults)
    cors_allowed_origins: list[str] = ["http://localhost:3000", "http://localhost:5173"]

    # ML inference (CNN-LSTM; optional; leave unset to use stub)
    ml_model_path: str | None = None
    inference_batch_size: int = 16
    tf_cpp_min_log_level: str = "2"
    tf_enable_onednn_opts: int | None = None

    # Video preprocessing (frame extraction and normalization for ML)
    frame_extract_fps: float = 2.0
    model_input_size: int = 64
    max_frames: int = 32

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )


# Global settings instance
settings = Settings()
