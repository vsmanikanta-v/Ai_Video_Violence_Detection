"""AI Video Violence Detection FastAPI Application.

Main application entry point with OpenAPI configuration,
endpoint registration, and middleware setup.
"""

import logging
from contextlib import asynccontextmanager

import yaml
from app.config import settings
from app.limiter import limiter
from app.routers import admin, auth, detections, health, videos
from app.services.auth_service import register_user
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

logger = logging.getLogger(__name__)


async def _ensure_default_users() -> None:  # noqa: C901
    """Create default admin and user accounts if configured and they do not exist."""
    if not settings.create_default_users:
        return
    admin_password = settings.default_admin_password
    user_password = settings.default_user_password
    if not admin_password or not user_password:
        logger.warning(
            "CREATE_DEFAULT_USERS is enabled but DEFAULT_ADMIN_PASSWORD/DEFAULT_USER_PASSWORD "
            "are not set. Skipping default user creation."
        )
        return
    # Create default admin (ignore if already exists)
    try:
        register_user(
            settings.default_admin_username,
            settings.default_admin_email,
            admin_password,
            "ADMIN",
        )
        logger.info("Created default admin user: %s", settings.default_admin_username)
    except HTTPException as e:
        if e.status_code == 409:
            logger.debug("Default admin already exists, skipping.")
        else:
            logger.warning("Could not create default admin: %s", e)
    except Exception as e:
        logger.warning("Could not create default admin: %s", e)

    # Create default user (ignore if already exists)
    try:
        register_user(
            settings.default_user_username,
            settings.default_user_email,
            user_password,
            "USER",
        )
        logger.info("Created default user: %s", settings.default_user_username)
    except HTTPException as e:
        if e.status_code == 409:
            logger.debug("Default user already exists, skipping.")
        else:
            logger.warning("Could not create default user: %s", e)
    except Exception as e:
        logger.warning("Could not create default user: %s", e)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup: create default users if configured. Shutdown: nothing."""
    await _ensure_default_users()
    yield


# Initialize FastAPI app with OpenAPI metadata
app = FastAPI(
    lifespan=lifespan,
    title="AI Video Violence Detection API",
    description=(
        "N-Tier API for video violence detection with CNN-LSTM (Keras inference) and optional "
        "Google Gemini incident explanations. Supports registration, JWT auth, video upload/analysis, "
        "detection history, and admin audit endpoints."
    ),
    version="1.0.0",
    contact={
        "name": "Viswanatha Swamy P K",
        "email": "support@ai-video-violence-detection.com",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
    openapi_tags=[
        {
            "name": "System",
            "description": "System health and metadata endpoints",
        },
        {
            "name": "Authentication",
            "description": "User registration, login, and profile management",
        },
        {
            "name": "Videos",
            "description": "Video upload, analysis, and history",
        },
        {
            "name": "Detections",
            "description": "Retrieve detection results by result ID or video ID",
        },
        {
            "name": "Admin",
            "description": "Admin-only audit logs and activity metrics",
        },
        {
            "name": "Documentation",
            "description": "API documentation and OpenAPI specification",
        },
    ],
    docs_url="/api/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type", "X-Request-ID"],
)

# Register routers
app.include_router(health.router)
app.include_router(auth.router)
app.include_router(videos.router)
app.include_router(detections.router)
app.include_router(admin.router)


@app.get(
    "/",
    tags=["System"],
    summary="Root endpoint with API metadata",
    description="Returns API information and navigation links to documentation and endpoints.",
    responses={
        200: {
            "description": "API information",
            "content": {
                "application/json": {
                    "example": {
                        "status": "ok",
                        "message": "AI Video Violence Detection API",
                        "version": "1.0.0",
                        "endpoints": {
                            "health": "/health",
                            "openapi": "/api/openapi.yaml",
                            "swagger": "/api/docs",
                            "redoc": "/redoc",
                        },
                    }
                }
            },
        }
    },
)
async def root() -> dict:
    """Root endpoint with API metadata.

    Returns:
        Dictionary with API information and endpoint links
    """
    return {
        "status": "ok",
        "message": "AI Video Violence Detection API",
        "version": app.version,
        "endpoints": {
            "health": "/health",
            "openapi": "/api/openapi.yaml",
            "swagger": "/api/docs",
            "redoc": "/redoc",
        },
    }


@app.get(
    "/api/openapi.yaml",
    tags=["Documentation"],
    summary="Get OpenAPI 3.1 specification in YAML format",
    description="Download the complete OpenAPI specification in YAML format.",
    response_class=PlainTextResponse,
    responses={
        200: {
            "description": "OpenAPI YAML specification",
            "content": {"application/x-yaml": {"schema": {"type": "string"}}},
        }
    },
)
async def get_openapi_yaml() -> PlainTextResponse:
    """Get OpenAPI specification in YAML format.

    Returns:
        YAML formatted OpenAPI specification
    """
    openapi_schema = app.openapi()

    # Add security schemes
    if "components" not in openapi_schema:
        openapi_schema["components"] = {}
    if "securitySchemes" not in openapi_schema["components"]:
        openapi_schema["components"]["securitySchemes"] = {}

    openapi_schema["components"]["securitySchemes"]["bearerAuth"] = {
        "type": "http",
        "scheme": "bearer",
        "bearerFormat": "JWT",
        "description": "Enter JWT token obtained from /api/auth/login or /api/auth/register",
    }

    # Convert to YAML
    yaml_content = yaml.dump(openapi_schema, sort_keys=False, default_flow_style=False)

    return PlainTextResponse(content=yaml_content, media_type="application/x-yaml")
