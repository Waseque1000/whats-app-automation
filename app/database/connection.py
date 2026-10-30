"""Database connection manager for SQLite."""
import sqlite3
from pathlib import Path
from typing import Optional
import os
from app.utils.logger import logger

DEFAULT_DB_PATH = Path(__file__).resolve().parent.parent.parent / "data" / "app.db"

class DatabaseManager:
    """Manages SQLite connections with thread safety and appropriate PRAGMAs."""
    def __init__(self, db_path: Optional[str] = None):
        if db_path:
            self.db_path = Path(db_path)
        else:
            env_path = os.getenv("DATABASE_PATH")
            self.db_path = Path(env_path) if env_path else DEFAULT_DB_PATH

        self.db_path.parent.mkdir(parents=True, exist_ok=True)

    def get_connection(self) -> sqlite3.Connection:
        """Returns a new sqlite3 connection with Row factory and WAL mode enabled."""
        conn = sqlite3.connect(
            str(self.db_path),
            check_same_thread=False,
            timeout=30.0,
        )
        conn.row_factory = sqlite3.Row
        # Enable foreign keys and WAL journal mode
        conn.execute("PRAGMA foreign_keys = ON;")
        conn.execute("PRAGMA journal_mode = WAL;")
        conn.execute("PRAGMA synchronous = NORMAL;")
        return conn

# Shared singleton instance
db_manager = DatabaseManager()

def get_db_connection() -> sqlite3.Connection:
    """Convenience helper to acquire a connection."""
    return db_manager.get_connection()
