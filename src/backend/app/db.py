"""Shared database connection helper.

Used by auth, video, and audit services to avoid duplication.
"""

import logging

import psycopg2
from app.config import settings
from fastapi import HTTPException, status

logger = logging.getLogger(__name__)


def get_db_connection():
    """Create a database connection.

    Returns:
        psycopg2 connection object

    Raises:
        HTTPException: 503 if database connection fails
    """
    try:
        return psycopg2.connect(settings.database_url)
    except psycopg2.Error as e:
        logger.error("Database connection failed: %s", e)
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database connection failed",
        )
