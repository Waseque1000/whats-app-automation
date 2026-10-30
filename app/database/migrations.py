"""Migration runner for SQLite schema."""
import sqlite3
from app.database.schema import MIGRATIONS
from app.utils.logger import logger

def run_migrations(conn: sqlite3.Connection) -> int:
    """
    Runs any pending migrations sequentially.
    Returns the latest applied schema version.
    """
    cursor = conn.cursor()

    # Ensure schema_version table exists
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS schema_version (
            version INTEGER PRIMARY KEY,
            applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    conn.commit()

    cursor.execute("SELECT MAX(version) FROM schema_version;")
    current_version = cursor.fetchone()[0] or 0
    logger.info(f"Current database schema version: {current_version}")

    applied_count = 0
    for version, sql_script in sorted(MIGRATIONS, key=lambda m: m[0]):
        if version > current_version:
            logger.info(f"Applying database migration version {version}...")
            try:
                conn.execute("BEGIN;")
                conn.executescript(sql_script)
                conn.execute(
                    "INSERT INTO schema_version (version) VALUES (?);", (version,)
                )
                conn.commit()
                current_version = version
                applied_count += 1
                logger.info(f"Successfully applied migration version {version}.")
            except Exception as exc:
                conn.rollback()
                logger.error(f"Migration version {version} failed: {exc}", exc_info=True)
                raise exc

    if applied_count == 0:
        logger.info("Database schema is up to date.")
    else:
        logger.info(f"Finished applying {applied_count} migrations. Current version: {current_version}")

    return current_version
