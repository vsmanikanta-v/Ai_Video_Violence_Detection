"""Audit logging for video upload and detection events."""

import logging

from app.db import get_db_connection

logger = logging.getLogger(__name__)


def log_action(
    user_id: int | None,
    action: str,
    entity_type: str | None = None,
    entity_id: int | None = None,
    request_context_id: str | None = None,
    details: str | None = None,
) -> None:
    """Write an audit log entry. Does not raise on failure (logs and returns).

    Args:
        user_id: User who performed the action (optional)
        action: Action name (e.g. video_uploaded, video_analyzed)
        entity_type: Type of entity (e.g. video, result)
        entity_id: ID of entity
        request_context_id: Correlation ID for the request
        details: Optional JSON or text details
    """
    conn = None
    cur = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO audit_logs (user_id, action, entity_type, entity_id, request_context_id, details)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (user_id, action, entity_type, entity_id, request_context_id, details),
        )
        conn.commit()
    except Exception as e:
        if conn:
            conn.rollback()
        # Do not fail the request; audit is best-effort
        logger.warning("Audit log write failed: %s", e)
    finally:
        if cur:
            try:
                cur.close()
            except Exception:
                pass
        if conn:
            try:
                conn.close()
            except Exception:
                pass
