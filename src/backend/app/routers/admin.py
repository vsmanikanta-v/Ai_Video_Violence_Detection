"""Admin-only API: audit logs and activity stats.

All routes require ADMIN role; return 403 for non-admin.
"""

from typing import Annotated

from app.deps import require_admin
from app.models.auth import User
from app.services.admin_service import get_admin_stats, get_audit_logs
from fastapi import APIRouter, Depends, Query

router = APIRouter(prefix="/api/admin", tags=["Admin"])


@router.get(
    "/stats",
    summary="Admin activity metrics",
    description="Aggregate counts (users, videos, results, audit logs). Admin only.",
    responses={
        200: {"description": "Key metrics"},
        401: {"description": "Unauthorized"},
        403: {"description": "Admin required"},
    },
)
async def admin_stats(_admin: Annotated[User, Depends(require_admin)]) -> dict:
    """Return counts for dashboard. No PII."""
    return get_admin_stats()


@router.get(
    "/audit-logs",
    summary="List audit logs",
    description="Recent audit log entries (paginated). Admin only. Minimal PII (username only).",
    responses={
        200: {"description": "List of audit log entries"},
        401: {"description": "Unauthorized"},
        403: {"description": "Admin required"},
    },
)
async def admin_audit_logs(
    _admin: Annotated[User, Depends(require_admin)],
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
) -> list[dict]:
    """Return audit logs, most recent first."""
    return get_audit_logs(limit=limit, offset=offset)
