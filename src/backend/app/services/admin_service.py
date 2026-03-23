"""Admin-only data access: audit logs and aggregate stats.

Minimal PII: audit log list includes username (for who did it) but not email.
"""

import logging

import psycopg2
from app.db import get_db_connection
from fastapi import HTTPException, status

logger = logging.getLogger(__name__)


def get_audit_logs(limit: int = 50, offset: int = 0) -> list[dict]:
    """Return audit log rows (recent first) with username when available. No email."""
    conn = None
    cur = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            """
            SELECT a.id, a.user_id, u.username, a.action, a.entity_type, a.entity_id,
                   a.request_context_id, a.details, a.created_at
            FROM audit_logs a
            LEFT JOIN users u ON u.id = a.user_id
            ORDER BY a.created_at DESC
            LIMIT %s OFFSET %s
            """,
            (limit, offset),
        )
        rows = cur.fetchall()
        return [
            {
                "id": r[0],
                "user_id": r[1],
                "username": r[2],
                "action": r[3],
                "entity_type": r[4],
                "entity_id": r[5],
                "request_context_id": r[6],
                "details": r[7],
                "created_at": r[8].isoformat() if r[8] else None,
            }
            for r in rows
        ]
    except psycopg2.Error as e:
        logger.error("Database error in get_audit_logs: %s", e)
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database error",
        )
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()


def get_admin_stats() -> dict:
    """Return aggregate counts for admin dashboard in a single query. No PII."""
    conn = None
    cur = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT
                (SELECT COUNT(*) FROM users)      AS total_users,
                (SELECT COUNT(*) FROM videos)     AS total_videos,
                (SELECT COUNT(*) FROM results)    AS total_results,
                (SELECT COUNT(*) FROM audit_logs) AS total_audit_logs
            """)
        row = cur.fetchone()
        return {
            "total_users": row[0],
            "total_videos": row[1],
            "total_results": row[2],
            "total_audit_logs": row[3],
        }
    except psycopg2.Error as e:
        logger.error("Database error in get_admin_stats: %s", e)
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database error",
        )
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
