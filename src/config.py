import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

WEBHOOK_URL = os.getenv("WEBHOOK_URL")
DROP_URL = os.getenv("DROP_URL", "https://store.epicgames.com/")
ROLE_ID = os.getenv("ROLE_ID")
CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL", 3600))

if not WEBHOOK_URL:
    raise ValueError("WEBHOOK_URL is not set. Please configure it in the .env file.")