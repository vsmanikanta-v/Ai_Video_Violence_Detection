"""Authentication router for user registration, login, profile management, and RBAC."""

from typing import Annotated

from app.deps import require_admin
from app.models.auth import AuthResponse, LoginRequest, RegisterRequest, User
from app.services.auth_service import authenticate_user, get_user_by_id, register_user
from app.utils.jwt_handler import create_access_token, get_current_user_id
from fastapi import APIRouter, Depends, HTTPException, status

router = APIRouter(prefix="/api/auth", tags=["Authentication"])


def _build_auth_token(user: User) -> str:
    """Build JWT access token payload from a user instance."""
    return create_access_token({"user_id": user.id, "username": user.username, "role": user.role})


@router.post(
    "/register",
    response_model=AuthResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user account",
    description=(
        "Create a new user account with username, email, and password. "
        "Returns JWT token upon successful registration."
    ),
    responses={
        201: {
            "description": "User successfully registered",
            "content": {
                "application/json": {
                    "example": {
                        "user": {
                            "id": 1,
                            "username": "john_doe",
                            "email": "john.doe@company.com",
                            "role": "USER",
                            "created_at": "2026-02-12T10:00:00Z",
                        },
                        "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                        "token_type": "bearer",
                    }
                }
            },
        },
        400: {"description": "Validation error (invalid input)"},
        409: {"description": "User already exists (duplicate username/email)"},
    },
)
async def register(request: RegisterRequest) -> AuthResponse:
    """Register a new user account.

    Args:
        request: Registration request with username, email, password, and role

    Returns:
        AuthResponse with user information and JWT token

    Raises:
        HTTPException: 409 if username or email already exists
        HTTPException: 400 if validation fails
    """
    # Register user
    user = register_user(request.username, request.email, request.password, request.role)
    access_token = _build_auth_token(user)
    return AuthResponse(user=user, access_token=access_token, token_type="bearer")


@router.post(
    "/login",
    response_model=AuthResponse,
    summary="Authenticate user and return JWT token",
    description="Login with username and password. Returns JWT token upon successful authentication.",
    responses={
        200: {
            "description": "Login successful",
            "content": {
                "application/json": {
                    "example": {
                        "user": {
                            "id": 1,
                            "username": "john_doe",
                            "email": "john.doe@company.com",
                            "role": "USER",
                            "created_at": "2026-02-12T10:00:00Z",
                        },
                        "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                        "token_type": "bearer",
                    }
                }
            },
        },
        400: {"description": "Validation error"},
        401: {"description": "Invalid credentials (wrong username/password)"},
    },
)
async def login(request: LoginRequest) -> AuthResponse:
    """Authenticate user with credentials.

    Args:
        request: Login request with username and password

    Returns:
        AuthResponse with user information and JWT token

    Raises:
        HTTPException: 401 if credentials are invalid
    """
    # Authenticate user
    user = authenticate_user(request.username, request.password)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = _build_auth_token(user)
    return AuthResponse(user=user, access_token=access_token, token_type="bearer")


@router.get(
    "/me",
    response_model=dict[str, User],
    summary="Get authenticated user information",
    description="Get the current user's profile information. Requires valid JWT token in Authorization header.",
    responses={
        200: {
            "description": "Current user information",
            "content": {
                "application/json": {
                    "example": {
                        "user": {
                            "id": 1,
                            "username": "john_doe",
                            "email": "john.doe@company.com",
                            "role": "USER",
                            "created_at": "2026-02-12T10:00:00Z",
                        }
                    }
                }
            },
        },
        401: {"description": "Unauthorized (missing or invalid token)"},
    },
)
async def get_current_user(user_id: Annotated[int, Depends(get_current_user_id)]) -> dict[str, User]:
    """Get current authenticated user.

    Args:
        user_id: User ID extracted from JWT token (dependency)

    Returns:
        Dictionary with user information

    Raises:
        HTTPException: 401 if token is invalid
        HTTPException: 404 if user not found
    """
    user = get_user_by_id(user_id)

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return {"user": user}


@router.get(
    "/admin-check",
    summary="Admin-only endpoint (RBAC)",
    description="Returns 200 if the current user has ADMIN role; 403 otherwise. Use to verify admin access.",
    responses={
        200: {"description": "Admin access granted"},
        401: {"description": "Missing or invalid token"},
        403: {"description": "Admin role required"},
    },
)
async def admin_check(admin_user: Annotated[User, Depends(require_admin)]) -> dict:
    """Require ADMIN role to access. Future admin routes can use Depends(require_admin)."""
    return {"message": "Admin access granted", "user_id": admin_user.id}
