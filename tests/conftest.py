"""Pytest configuration and shared test fixtures."""
import pytest
import sqlite3
import tempfile
from pathlib import Path
from typing import Generator

from app.database.migrations import run_migrations
from app.database.repository import (
    StudentsRepository,
    CampaignsRepository,
    TemplatesRepository,
    ImportsRepository,
    SettingsRepository,
)
from app.messaging.mock_provider import MockProvider
from app.services.campaign_service import CampaignService
from app.services.import_service import ImportService
from app.services.validation_service import ValidationService
from app.services.report_service import ReportService

@pytest.fixture
def memory_db() -> Generator[sqlite3.Connection, None, None]:
    """Provides an isolated in-memory SQLite connection with migrations applied."""
    conn = sqlite3.connect(":memory:", check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    run_migrations(conn)
    yield conn
    conn.close()

@pytest.fixture
def students_repo(memory_db: sqlite3.Connection) -> StudentsRepository:
    return StudentsRepository(memory_db)

@pytest.fixture
def imports_repo(memory_db: sqlite3.Connection) -> ImportsRepository:
    return ImportsRepository(memory_db)

@pytest.fixture
def templates_repo(memory_db: sqlite3.Connection) -> TemplatesRepository:
    return TemplatesRepository(memory_db)

@pytest.fixture
def campaigns_repo(memory_db: sqlite3.Connection) -> CampaignsRepository:
    return CampaignsRepository(memory_db)

@pytest.fixture
def settings_repo(memory_db: sqlite3.Connection) -> SettingsRepository:
    return SettingsRepository(memory_db)

@pytest.fixture
def mock_provider() -> MockProvider:
    return MockProvider(simulate_latency_ms=0)

@pytest.fixture
def campaign_service(
    campaigns_repo: CampaignsRepository,
    students_repo: StudentsRepository,
    mock_provider: MockProvider,
) -> CampaignService:
    return CampaignService(campaigns_repo, students_repo, mock_provider)

@pytest.fixture
def import_service(
    students_repo: StudentsRepository,
    imports_repo: ImportsRepository,
) -> ImportService:
    return ImportService(students_repo, imports_repo, default_region="BD")

@pytest.fixture
def validation_service() -> ValidationService:
    return ValidationService(default_region="BD")

@pytest.fixture
def report_service(
    students_repo: StudentsRepository,
    campaigns_repo: CampaignsRepository,
) -> ReportService:
    return ReportService(students_repo, campaigns_repo)
