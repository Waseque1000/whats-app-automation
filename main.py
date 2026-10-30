"""Desktop application entrypoint for WhatsApp Student Messenger."""
import sys
import os
from pathlib import Path
from dotenv import load_dotenv

# Ensure application root is in python path
ROOT_DIR = Path(__file__).resolve().parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

# Load .env configuration if present
env_file = ROOT_DIR / ".env"
if env_file.exists():
    load_dotenv(env_file)
else:
    example_env = ROOT_DIR / ".env.example"
    if example_env.exists():
        load_dotenv(example_env)

from app.utils.logger import logger
from app.application import WhatsAppStudentMessengerApp

def main():
    """Main launcher function."""
    logger.info("Starting WhatsApp Student Messenger desktop application...")
    try:
        app = WhatsAppStudentMessengerApp()
        app.protocol("WM_DELETE_WINDOW", app.on_closing)
        app.mainloop()
    except Exception as exc:
        logger.critical(f"Unhandled fatal application crash: {exc}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()
