"""Shared database connection helper.

Used by auth, video, and audit services to avoid duplication.
"""

import logging
from pathlib import Path

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


def _get_schema_path() -> Path:
    """Return path to the local database schema SQL file."""
    return Path(__file__).resolve().parents[3] / "infra" / "database" / "schema.sql"


def ensure_database_schema() -> None:
    """Initialize the database schema if the users table does not exist."""
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT EXISTS (
                SELECT 1 FROM information_schema.tables
                WHERE table_schema = 'public' AND table_name = 'users'
            )
            """
        )

        if cursor.fetchone()[0]:
            return

        schema_path = _get_schema_path()
        if not schema_path.exists():
            logger.error("Database schema file not found: %s", schema_path)
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Database schema file missing",
            )

        with schema_path.open("r", encoding="utf-8") as schema_file:
            schema_sql = schema_file.read()

        cursor.execute(schema_sql)
        conn.commit()
        logger.info("Initialized database schema from %s", schema_path)
    except psycopg2.Error as e:
        if conn:
            conn.rollback()
        logger.error("Database schema initialization failed: %s", e)
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database schema initialization failed",
        )
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
