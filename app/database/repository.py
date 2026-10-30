"""Repository layer for SQLite database access."""
import sqlite3
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime
from app.utils.logger import logger

class Repository:
    """Base repository with access to SQLite connection."""
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn

class ImportsRepository(Repository):
    """Repository for import audit records."""

    def add_import(
        self,
        filename: str,
        total_rows: int,
        valid_rows: int,
        invalid_rows: int,
        duplicate_rows: int,
    ) -> int:
        cursor = self.conn.cursor()
        cursor.execute(
            """
            INSERT INTO imports (filename, total_rows, valid_rows, invalid_rows, duplicate_rows)
            VALUES (?, ?, ?, ?, ?);
            """,
            (filename, total_rows, valid_rows, invalid_rows, duplicate_rows),
        )
        self.conn.commit()
        return cursor.lastrowid

    def get_recent(self, limit: int = 5) -> List[Dict[str, Any]]:
        cursor = self.conn.cursor()
        cursor.execute(
            """
            SELECT id, filename, imported_at, total_rows, valid_rows, invalid_rows, duplicate_rows
            FROM imports
            ORDER BY imported_at DESC, id DESC
            LIMIT ?;
            """,
            (limit,),
        )
        return [dict(row) for row in cursor.fetchall()]

class StudentsRepository(Repository):
    """Repository for student records and filtering."""

    def find_by_phone(self, phone: str) -> Optional[Dict[str, Any]]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM students WHERE phone = ?;", (phone,))
        row = cursor.fetchone()
        return dict(row) if row else None

    def add_student(
        self,
        name: str,
        phone: str,
        raw_phone: str = "",
        email: Optional[str] = None,
        batch: Optional[str] = None,
        whatsapp_status: str = "unknown",
        consent_status: str = "unknown",
        is_valid: int = 1,
        validation_error: Optional[str] = None,
        is_duplicate: int = 0,
    ) -> int:
        cursor = self.conn.cursor()
        cursor.execute(
            """
            INSERT INTO students (
                name, phone, raw_phone, email, batch, whatsapp_status,
                consent_status, is_valid, validation_error, is_duplicate
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
            """,
            (
                name.strip(),
                phone.strip(),
                raw_phone.strip() if raw_phone else phone.strip(),
                email.strip() if email else None,
                batch.strip() if batch else None,
                whatsapp_status,
                consent_status,
                is_valid,
                validation_error,
                is_duplicate,
            ),
        )
        self.conn.commit()
        return cursor.lastrowid

    def update_student(
        self,
        student_id: int,
        name: Optional[str] = None,
        phone: Optional[str] = None,
        raw_phone: Optional[str] = None,
        email: Optional[str] = None,
        batch: Optional[str] = None,
        whatsapp_status: Optional[str] = None,
        consent_status: Optional[str] = None,
        is_valid: Optional[int] = None,
        validation_error: Optional[str] = None,
        is_duplicate: Optional[int] = None,
    ) -> None:
        updates = []
        params = []
        if name is not None:
            updates.append("name = ?")
            params.append(name.strip())
        if phone is not None:
            updates.append("phone = ?")
            params.append(phone.strip())
        if raw_phone is not None:
            updates.append("raw_phone = ?")
            params.append(raw_phone.strip())
        if email is not None:
            updates.append("email = ?")
            params.append(email.strip() if email else None)
        if batch is not None:
            updates.append("batch = ?")
            params.append(batch.strip() if batch else None)
        if whatsapp_status is not None:
            updates.append("whatsapp_status = ?")
            params.append(whatsapp_status)
        if consent_status is not None:
            updates.append("consent_status = ?")
            params.append(consent_status)
        if is_valid is not None:
            updates.append("is_valid = ?")
            params.append(is_valid)
        if validation_error is not None:
            updates.append("validation_error = ?")
            params.append(validation_error)
        if is_duplicate is not None:
            updates.append("is_duplicate = ?")
            params.append(is_duplicate)

        if not updates:
            return

        updates.append("updated_at = CURRENT_TIMESTAMP")
        params.append(student_id)
        sql = f"UPDATE students SET {', '.join(updates)} WHERE id = ?;"
        self.conn.execute(sql, params)
        self.conn.commit()

    def get_all(
        self,
        search: str = "",
        batch: str = "",
        consent_status: str = "",
        is_valid: Optional[int] = None,
        limit: Optional[int] = None,
        offset: int = 0,
    ) -> List[Dict[str, Any]]:
        query = "SELECT * FROM students WHERE 1=1"
        params: List[Any] = []

        if search:
            query += " AND (name LIKE ? OR phone LIKE ? OR raw_phone LIKE ? OR email LIKE ?)"
            term = f"%{search.strip()}%"
            params.extend([term, term, term, term])

        if batch:
            query += " AND batch = ?"
            params.append(batch.strip())

        if consent_status:
            query += " AND consent_status = ?"
            params.append(consent_status.strip())

        if is_valid is not None:
            query += " AND is_valid = ?"
            params.append(is_valid)

        query += " ORDER BY id DESC"
        if limit is not None:
            query += " LIMIT ? OFFSET ?"
            params.extend([limit, offset])

        cursor = self.conn.cursor()
        cursor.execute(query, params)
        return [dict(row) for row in cursor.fetchall()]

    def get_by_ids(self, student_ids: List[int]) -> List[Dict[str, Any]]:
        if not student_ids:
            return []
        placeholders = ",".join("?" for _ in student_ids)
        cursor = self.conn.cursor()
        cursor.execute(
            f"SELECT * FROM students WHERE id IN ({placeholders}) ORDER BY id ASC;",
            student_ids,
        )
        return [dict(row) for row in cursor.fetchall()]

    def get_batches(self) -> List[str]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT DISTINCT batch FROM students WHERE batch IS NOT NULL AND batch != '' ORDER BY batch ASC;")
        return [row[0] for row in cursor.fetchall()]

    def get_stats(self) -> Dict[str, Any]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM students;")
        total = cursor.fetchone()[0] or 0

        cursor.execute("SELECT COUNT(*) FROM students WHERE is_valid = 1;")
        valid = cursor.fetchone()[0] or 0

        cursor.execute("SELECT COUNT(*) FROM students WHERE is_valid = 0;")
        invalid = cursor.fetchone()[0] or 0

        cursor.execute("SELECT COUNT(*) FROM students WHERE is_duplicate = 1;")
        duplicates = cursor.fetchone()[0] or 0

        cursor.execute("SELECT COUNT(*) FROM students WHERE consent_status = 'granted';")
        consent_granted = cursor.fetchone()[0] or 0

        cursor.execute("SELECT COUNT(*) FROM students WHERE consent_status = 'opted_out';")
        consent_opted_out = cursor.fetchone()[0] or 0

        cursor.execute("SELECT COUNT(*) FROM students WHERE consent_status = 'unknown';")
        consent_unknown = cursor.fetchone()[0] or 0

        return {
            "total_students": total,
            "valid_formats": valid,
            "invalid_formats": invalid,
            "duplicates": duplicates,
            "consent_granted": consent_granted,
            "consent_opted_out": consent_opted_out,
            "consent_unknown": consent_unknown,
        }

class TemplatesRepository(Repository):
    """Repository for message templates."""

    def create(self, name: str, content: str, variables: str = "") -> int:
        cursor = self.conn.cursor()
        cursor.execute(
            """
            INSERT INTO templates (template_name, content, available_variables)
            VALUES (?, ?, ?);
            """,
            (name.strip(), content.strip(), variables.strip()),
        )
        self.conn.commit()
        return cursor.lastrowid

    def update(self, template_id: int, name: str, content: str, variables: str = "") -> None:
        self.conn.execute(
            """
            UPDATE templates
            SET template_name = ?, content = ?, available_variables = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?;
            """,
            (name.strip(), content.strip(), variables.strip(), template_id),
        )
        self.conn.commit()

    def delete(self, template_id: int) -> None:
        self.conn.execute("DELETE FROM templates WHERE id = ?;", (template_id,))
        self.conn.commit()

    def get_all(self) -> List[Dict[str, Any]]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM templates ORDER BY template_name ASC;")
        return [dict(row) for row in cursor.fetchall()]

    def get_by_id(self, template_id: int) -> Optional[Dict[str, Any]]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM templates WHERE id = ?;", (template_id,))
        row = cursor.fetchone()
        return dict(row) if row else None

class CampaignsRepository(Repository):
    """Repository for campaign creation, queues, and status audits."""

    def create(
        self,
        name: str,
        message_template: str,
        template_id: Optional[int],
        total_recipients: int,
        confirmed_at: Optional[str] = None,
    ) -> int:
        cursor = self.conn.cursor()
        cursor.execute(
            """
            INSERT INTO campaigns (campaign_name, message_template, template_id, status, total_recipients, confirmed_at)
            VALUES (?, ?, ?, 'draft', ?, ?);
            """,
            (name.strip(), message_template.strip(), template_id, total_recipients, confirmed_at),
        )
        self.conn.commit()
        return cursor.lastrowid

    def add_recipients(self, campaign_id: int, recipients: List[Dict[str, Any]]) -> None:
        """Batch insert recipient queue records."""
        cursor = self.conn.cursor()
        cursor.executemany(
            """
            INSERT INTO campaign_recipients (campaign_id, student_id, phone, personalized_message, status)
            VALUES (?, ?, ?, ?, ?);
            """,
            [
                (
                    campaign_id,
                    r.get("student_id"),
                    r["phone"],
                    r["personalized_message"],
                    r.get("status", "pending"),
                )
                for r in recipients
            ],
        )
        self.conn.commit()

    def update_campaign_status(
        self,
        campaign_id: int,
        status: str,
        completed_at: Optional[str] = None,
    ) -> None:
        params: List[Any] = [status]
        sql = "UPDATE campaigns SET status = ?"
        if completed_at is not None:
            sql += ", completed_at = ?"
            params.append(completed_at)
        sql += " WHERE id = ?;"
        params.append(campaign_id)
        self.conn.execute(sql, params)
        self.conn.commit()

    def update_campaign_counts(
        self,
        campaign_id: int,
        successful: int,
        failed: int,
        skipped: int,
    ) -> None:
        self.conn.execute(
            """
            UPDATE campaigns
            SET successful_recipients = ?, failed_recipients = ?, skipped_recipients = ?
            WHERE id = ?;
            """,
            (successful, failed, skipped, campaign_id),
        )
        self.conn.commit()

    def record_confirmation(self, campaign_id: int, confirmed_at: Optional[str] = None) -> None:
        ts = confirmed_at or datetime.now().isoformat()
        self.conn.execute(
            "UPDATE campaigns SET confirmed_at = ?, status = 'queued' WHERE id = ?;",
            (ts, campaign_id),
        )
        self.conn.commit()

    def update_recipient_status(
        self,
        recipient_id: int,
        status: str,
        error_message: Optional[str] = None,
        sent_at: Optional[str] = None,
    ) -> None:
        self.conn.execute(
            """
            UPDATE campaign_recipients
            SET status = ?, error_message = ?, sent_at = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?;
            """,
            (status, error_message, sent_at, recipient_id),
        )
        self.conn.commit()

    def get_campaign(self, campaign_id: int) -> Optional[Dict[str, Any]]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM campaigns WHERE id = ?;", (campaign_id,))
        row = cursor.fetchone()
        return dict(row) if row else None

    def get_campaigns(self, limit: int = 50) -> List[Dict[str, Any]]:
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT * FROM campaigns ORDER BY id DESC LIMIT ?;",
            (limit,),
        )
        return [dict(row) for row in cursor.fetchall()]

    def get_recipients(self, campaign_id: int) -> List[Dict[str, Any]]:
        cursor = self.conn.cursor()
        cursor.execute(
            """
            SELECT cr.*, s.name as student_name, s.batch as student_batch, s.consent_status
            FROM campaign_recipients cr
            LEFT JOIN students s ON cr.student_id = s.id
            WHERE cr.campaign_id = ?
            ORDER BY cr.id ASC;
            """,
            (campaign_id,),
        )
        return [dict(row) for row in cursor.fetchall()]

    def get_stats(self) -> Dict[str, Any]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM campaigns;")
        total_campaigns = cursor.fetchone()[0] or 0

        cursor.execute("SELECT COUNT(*) FROM campaign_recipients WHERE status IN ('sent', 'delivered', 'read');")
        messages_sent = cursor.fetchone()[0] or 0

        cursor.execute("SELECT COUNT(*) FROM campaign_recipients WHERE status = 'submitted';")
        messages_submitted = cursor.fetchone()[0] or 0

        cursor.execute("SELECT COUNT(*) FROM campaign_recipients WHERE status = 'failed';")
        messages_failed = cursor.fetchone()[0] or 0

        return {
            "total_campaigns": total_campaigns,
            "messages_sent": messages_sent,
            "messages_submitted": messages_submitted,
            "messages_failed": messages_failed,
        }

class SettingsRepository(Repository):
    """Repository for key-value application settings."""

    def get(self, key: str, default: Optional[str] = None) -> Optional[str]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT value FROM settings WHERE key = ?;", (key,))
        row = cursor.fetchone()
        return row[0] if row else default

    def set(self, key: str, value: str) -> None:
        self.conn.execute(
            """
            INSERT INTO settings (key, value, updated_at)
            VALUES (?, ?, CURRENT_TIMESTAMP)
            ON CONFLICT(key) DO UPDATE SET value = excluded.value, updated_at = CURRENT_TIMESTAMP;
            """,
            (key, str(value)),
        )
        self.conn.commit()

    def get_all(self) -> Dict[str, str]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT key, value FROM settings;")
        return {row["key"]: row["value"] for row in cursor.fetchall()}
