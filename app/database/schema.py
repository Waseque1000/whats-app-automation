"""Database schema definitions and migration scripts."""

# List of migrations as (version: int, sql: str) tuples
MIGRATIONS = [
    (
        1,
        """
        -- Schema version tracking
        CREATE TABLE IF NOT EXISTS schema_version (
            version INTEGER PRIMARY KEY,
            applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        -- Imports history table
        CREATE TABLE IF NOT EXISTS imports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT NOT NULL,
            imported_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            total_rows INTEGER NOT NULL DEFAULT 0,
            valid_rows INTEGER NOT NULL DEFAULT 0,
            invalid_rows INTEGER NOT NULL DEFAULT 0,
            duplicate_rows INTEGER NOT NULL DEFAULT 0
        );

        -- Students records table
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            raw_phone TEXT,
            email TEXT,
            batch TEXT,
            whatsapp_status TEXT NOT NULL DEFAULT 'unknown',
            consent_status TEXT NOT NULL DEFAULT 'unknown',
            is_valid INTEGER NOT NULL DEFAULT 1,
            validation_error TEXT,
            is_duplicate INTEGER NOT NULL DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE INDEX IF NOT EXISTS idx_students_phone ON students(phone);
        CREATE INDEX IF NOT EXISTS idx_students_consent ON students(consent_status);
        CREATE INDEX IF NOT EXISTS idx_students_batch ON students(batch);

        -- Message templates table
        CREATE TABLE IF NOT EXISTS templates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            template_name TEXT NOT NULL UNIQUE,
            content TEXT NOT NULL,
            available_variables TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        -- Campaigns table
        CREATE TABLE IF NOT EXISTS campaigns (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            campaign_name TEXT NOT NULL,
            message_template TEXT NOT NULL,
            template_id INTEGER REFERENCES templates(id) ON DELETE SET NULL,
            status TEXT NOT NULL DEFAULT 'draft',
            total_recipients INTEGER NOT NULL DEFAULT 0,
            successful_recipients INTEGER NOT NULL DEFAULT 0,
            failed_recipients INTEGER NOT NULL DEFAULT 0,
            skipped_recipients INTEGER NOT NULL DEFAULT 0,
            confirmed_at TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            completed_at TIMESTAMP
        );

        -- Campaign recipients queue and audit table
        CREATE TABLE IF NOT EXISTS campaign_recipients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            campaign_id INTEGER NOT NULL REFERENCES campaigns(id) ON DELETE CASCADE,
            student_id INTEGER REFERENCES students(id) ON DELETE SET NULL,
            phone TEXT NOT NULL,
            personalized_message TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'pending',
            error_message TEXT,
            sent_at TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE INDEX IF NOT EXISTS idx_campaign_recipients_campaign ON campaign_recipients(campaign_id);
        CREATE INDEX IF NOT EXISTS idx_campaign_recipients_status ON campaign_recipients(status);

        -- Application settings table
        CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        -- Insert default initial settings
        INSERT OR IGNORE INTO settings (key, value) VALUES ('default_region', 'BD');
        INSERT OR IGNORE INTO settings (key, value) VALUES ('provider', 'mock');
        INSERT OR IGNORE INTO settings (key, value) VALUES ('confirm_each_campaign', 'true');
        INSERT OR IGNORE INTO settings (key, value) VALUES ('theme', 'dark');
        """
    )
]
