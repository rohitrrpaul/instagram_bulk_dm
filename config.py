import os
from pathlib import Path

# Base directories
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
LOGS_DIR = BASE_DIR / "logs"

# Create directories if they don't exist
DATA_DIR.mkdir(exist_ok=True)
LOGS_DIR.mkdir(exist_ok=True)

# File paths
INPUT_CSV = DATA_DIR / "input.csv"
OUTPUT_CSV = DATA_DIR / "output.csv"
LOG_FILE = LOGS_DIR / "instagram_dm.log"

# Instagram settings
INSTAGRAM_URL = "https://www.instagram.com"
LOGIN_URL = f"{INSTAGRAM_URL}/accounts/login/"

# Timing settings (in seconds)
MIN_DELAY = 20
MAX_DELAY = 60
TYPING_DELAY_MIN = 0.1
TYPING_DELAY_MAX = 0.3
MAX_DMS_PER_HOUR = 20

# Browser settings
WINDOW_SIZE = (1920, 1080)
HEADLESS = False

# Message settings
MAX_RETRIES = 3
RETRY_DELAY = 300  # 5 minutes 