"""
PhishGuard AuditService — Structured security event logging service.

Listens on gRPC port 50052. Receives audit events from the FastAPI gateway
and stores them in a dedicated audit_log table (SQLite).

Events logged:
- USER_REGISTERED
- USER_LOGIN / USER_LOGIN_FAILED
- EMAIL_ANALYZED
- UNAUTHORIZED_ACCESS
- SERVICE_ERROR
"""
import sys
import os
import grpc
from concurrent import futures
import logging
import sqlite3

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'protos'))

from protos import audit_pb2
from protos import audit_pb2_grpc

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'phishguard.db')


def init_audit_db():
    """Create the audit_log table if it doesn't exist."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS audit_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_type VARCHAR(50) NOT NULL,
            username VARCHAR(100),
            details TEXT,
            ip_address VARCHAR(45),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()
    logger.info("audit_log table initialised.")


class AuditServiceServicer(audit_pb2_grpc.AuditServiceServicer):
    def __init__(self):
        init_audit_db()

    def LogEvent(self, request, context):
        event_type = request.event_type
        username = request.username or "anonymous"
        details = (request.details or "")[:500]  # truncate to prevent abuse
        ip_address = request.ip_address or "unknown"

        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO audit_log (event_type, username, details, ip_address) VALUES (?, ?, ?, ?)",
                (event_type, username, details, ip_address)
            )
            conn.commit()
            conn.close()
            logger.info(f"AUDIT: [{event_type}] user={username} ip={ip_address} — {details[:80]}")
            return audit_pb2.AuditResponse(success=True, message="Event logged")
        except Exception as e:
            logger.error(f"AUDIT LOG FAILED: {e}")
            return audit_pb2.AuditResponse(success=False, message="Logging failed")


def serve():
    init_audit_db()
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=5))
    audit_pb2_grpc.add_AuditServiceServicer_to_server(AuditServiceServicer(), server)
    server.add_insecure_port('[::]:50052')
    server.start()
    logger.info("AuditService gRPC server started on port 50052")
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
