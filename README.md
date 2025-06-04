# Instagram Bulk DM Bot

A Python-based automation tool for sending bulk direct messages on Instagram with anti-detection measures and human-like behavior simulation.

## Features

- 🔒 Anti-detection measures to avoid Instagram's automation detection
- 🤖 Human-like behavior simulation (typing, mouse movements, scrolling)
- 📊 Progress tracking and resume capability
- ⏱️ Rate limiting and session management
- 📝 Detailed logging
- 🔄 Auto-relogin functionality
- 🎯 Random delays and breaks to appear more natural

## Prerequisites

- Python 3.8 or higher
- Chrome browser installed
- Instagram account
- CSV file with target usernames and messages

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd instagram_bulk_dm
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

## Configuration

1. Create a `config.py` file with the following settings:
```python
# Instagram URLs
INSTAGRAM_URL = "https://www.instagram.com"
LOGIN_URL = "https://www.instagram.com/accounts/login/"

# File paths
INPUT_CSV = "data/input.csv"
OUTPUT_CSV = "data/output.csv"
LOG_FILE = "logs/instagram_dm.log"

# Rate limiting
MAX_DMS_PER_HOUR = 20
MIN_DELAY = 30
MAX_DELAY = 60
TYPING_DELAY_MIN = 0.1
TYPING_DELAY_MAX = 0.3
MAX_SESSION_HOURS = 4
MIN_ACTION_INTERVAL = 2

# Browser settings
HEADLESS = False
WINDOW_SIZE = (1200, 800)
```

2. Create the required directories:
```bash
mkdir -p data logs
```

3. Create an input CSV file (`data/input.csv`) with the following format:
```csv
username,message
user1,Hello! This is a test message.
user2,Hi there! How are you?
```

## Usage

1. Run the script:
```bash
python instagram_dm_bot.py
```

2. The script will:
   - Log in to Instagram
   - Process profiles from the input CSV
   - Save progress after each message
   - Handle session timeouts automatically
   - Create detailed logs

## Safety Features

- Random delays between actions
- Human-like typing with occasional mistakes
- Natural mouse movements
- Random scrolling
- Session management
- Rate limiting
- Progress tracking
- Auto-relogin capability

## Important Notes

1. **Rate Limits**: 
   - Default limit is 20 DMs per hour
   - Adjust `MAX_DMS_PER_HOUR` in config.py if needed
   - Script includes random delays between messages

2. **Session Management**:
   - Script automatically handles session timeouts
   - Auto-relogin functionality included
   - Progress is saved after each message

3. **Anti-Detection**:
   - Uses undetected-chromedriver
   - Simulates human behavior
   - Random delays and breaks
   - Natural mouse movements

4. **Progress Tracking**:
   - Progress saved in `data/output.csv`
   - Can resume from last successful message
   - Detailed logging in `logs/instagram_dm.log`

## Troubleshooting

1. **Login Issues**:
   - Check your credentials
   - Ensure 2FA is disabled
   - Try increasing delays in config

2. **Session Timeouts**:
   - Script will attempt to relogin automatically
   - Progress is saved before timeout
   - Can resume from last successful message

3. **Rate Limiting**:
   - Reduce `MAX_DMS_PER_HOUR` if getting blocked
   - Increase `MIN_DELAY` and `MAX_DELAY`
   - Add more random breaks

## Custom Requirements

For any custom requirements, feature requests, or modifications, please contact:
- Email: rohit.paul@excelloite.com

## Disclaimer

This tool is for educational purposes only. Use it responsibly and in accordance with Instagram's terms of service. Excessive automation may lead to account restrictions or bans.

## License

MIT License - See LICENSE file for details 