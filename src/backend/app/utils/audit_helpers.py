"""Audit log re-export for route modules.

Routes can import create_audit_log from here rather than reaching into services.
"""

from app.services.audit_service import log_action as create_audit_log

__all__ = ["create_audit_log"]
