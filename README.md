# WhatsApp Student Messenger (MVP)

A secure, local-first Python desktop application built for student contact management, phone normalization, templated message authoring, and compliant campaign preparation.

---

## Key Features

- **Dark Mode Dashboard:** CustomTkinter interface styled according to the Obsidian Signal dark theme design system (`#0B0F14` background, `#111820` sidebar, `#161F29` cards, `#25D366` emerald accents).
- **Manual Student Entry:** Direct form in the Students Registry allowing instant addition of student records with real-time E.164 normalization preview, batch assignment, consent status, and duplicate conflict prompts.
- **Multi-Format Ingestion:** Import student lists from `.xlsx`, `.xls` (via `xlrd`), and `.csv` spreadsheets with interactive column mapping, live preview, and error reports.
- **Phone Normalization & Duplicates:** Normalizes phone numbers to standard E.164 using Google's `phonenumbers` library with configurable default fallback regions (e.g. Bangladesh `BD`, United States `US`). Unparseable numbers are clearly flagged rather than dropped. Supports 3 duplicate resolution modes: *Skip*, *Update*, and *Keep Both (Flagged)*.
- **Templates with Placeholders:** Dynamic tags (`{{name}}`, `{{phone}}`, `{{email}}`, `{{batch}}`), real-time syntax validation, unknown variable warnings, and live student preview.
- **Compliance & Consent Enforcement:** Strictly forbids opted-out students (`consent_status == 'opted_out'`) at the service layer. Highlights unknown-consent students on review.
- **Explicit Campaign Confirmation:** Mandatory review screen summarizing recipient count, template body, and consent warnings, recorded with a verified timestamp.
- **Background Execution:** Multi-threaded import and dispatch queue keeps the desktop interface smooth and responsive with progress indicators, pause, and cancel controls.
- **Messaging Layer & MockProvider:** Clean `BaseMessagingProvider` abstraction with a `MockProvider` that only emits verified statuses (`sent`, `submitted`, `failed`, `skipped`). Never fabricates `delivered` or `read` receipts.
- **Export Parity:** One-click CSV and XLSX exports of student registers and campaign reports that exactly match the SQLite database schema.

---

## Project Structure

```text
whatsapp-student-messenger/
├── main.py                         # Desktop application launcher
├── requirements.txt                # Python package dependencies
├── README.md                       # Documentation & instructions
├── .env.example                    # Environment variable template
├── .gitignore                      # Git ignore rules (data/, *.db, logs)
├── pytest.ini                      # Pytest runner settings
├── whatsapp_messenger.spec         # PyInstaller desktop bundling spec
├── app/
│   ├── application.py              # Main CustomTkinter shell controller
│   ├── ui/
│   │   ├── theme.py                # Color palette & font constants
│   │   ├── dashboard.py            # Overview metrics & recent imports
│   │   ├── students_page.py        # Student registry & import modal
│   │   ├── campaigns_page.py       # Campaign wizard & live monitor
│   │   ├── templates_page.py       # Template editor & live preview
│   │   ├── reports_page.py         # History & data exports
│   │   ├── settings_page.py        # Region & provider settings
│   │   └── components/
│   │       ├── sidebar.py          # Left-hand navigation rail
│   │       ├── stat_card.py        # KPI metric card widget
│   │       ├── table_view.py       # Dark-styled Treeview table
│   │       └── modal_dialog.py     # Base modal dialog window
│   ├── services/
│   │   ├── import_service.py       # File parsing, column mapping & duplicates
│   │   ├── validation_service.py   # E.164 phone & consent validation
│   │   ├── template_service.py     # Placeholder regex & substitution
│   │   ├── campaign_service.py     # Opt-out filtering & queue worker
│   │   └── report_service.py       # CSV / XLSX exact export service
│   ├── messaging/
│   │   ├── base.py                 # Abstract BaseMessagingProvider & status enum
│   │   └── mock_provider.py        # Local simulation provider
│   ├── database/
│   │   ├── connection.py           # SQLite connection & WAL mode
│   │   ├── schema.py               # DDL schemas & migration scripts
│   │   ├── migrations.py           # Version-tracked migration runner
│   │   └── repository.py           # Typed SQLite CRUD repositories
│   └── utils/
│       ├── phone.py                # phonenumbers E.164 helper
│       ├── file_handler.py         # Multi-format spreadsheet reader
│       └── logger.py               # Rotating file logger (data/logs/app.log)
├── data/                           # Local database & logs (.gitignored)
└── tests/
    ├── conftest.py                 # In-memory test fixtures
    ├── test_import.py              # File ingestion & duplicate tests
    ├── test_validation.py          # E.164 normalization & regions tests
    ├── test_templates.py           # Substitution & invalid tags tests
    ├── test_campaigns.py           # Opt-out exclusion & confirmation tests
    └── test_reports.py             # Export database parity tests
```

---

## Setup & Running Locally

### 1. Requirements
- Python 3.12+ (installed via Homebrew or system)
- Tkinter support (`brew install python-tk@3.12` on macOS)

### 2. Virtual Environment Setup
```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Launch the Application
```bash
python main.py
```

---

## Running Automated Tests

Run the complete pytest test suite:
```bash
pytest -v
```

All 19 test cases verify:
- **Import Service:** `.csv` / `.xlsx` / `.xls` parsing, preservation of leading zeros, bad rows flagging, and duplicate resolution modes (`skip`, `update`, `keep_both_flagged`).
- **Validation:** Normalization across regions, detection of unparseable numbers without dropping records.
- **Templates:** Placeholder replacement, missing field fallbacks, and identification of unknown tags.
- **Campaigns:** Service-layer exclusion of opted-out recipients, mandatory confirmation logging, and status transitions.
- **Reports:** Parity between exported CSV/XLSX files and database tables.

---

## Building Desktop Executable

To package the desktop application into a standalone `.app` bundle on macOS:
```bash
pyinstaller whatsapp_messenger.spec
```
The compiled application will be generated in `dist/WhatsAppStudentMessenger.app`.
