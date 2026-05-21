# Telegram Weather Bot
A lightweight, modular Telegram bot for tracking weather forecasts at custom locations.

## Features
- **Interactive Menu**: Uses inline buttons for quick access to weather reports.
- **Multiple Views**: Supports Current, Daily (hourly breakdown), and Weekly forecasts.
- **Location Profiles**: Configured for two distinct locations (e.g., Home and Work).
- **Auto-Cleanup**: Automatically deletes weather reports from Telegram after 15 seconds for privacy and clutter reduction.

## Requirements
- Python 3.x
- telethon
- requests
- python-dotenv

## Setup

1. **Install Dependencies**:
   ```bash
   pip install telethon requests python-dotenv
Environment Configuration:
Create a .env file to store your sensitive credentials and paths:

### Code snippet
    ```
    DOTENV_FILE_PATH=path/to/your/.env
    private_app_id=YOUR_TELEGRAM_APP_ID
    private_app_hash=YOUR_TELEGRAM_APP_HASH
    tg_wtbot_token=YOUR_BOT_TOKEN
    tg_wtbot_session=bot_session
    tg_user_id=YOUR_TELEGRAM_USER_ID
    wt_path=python path/to/wtbot.py
    report=path/to/report.txt
    ir=LATITUDE LONGITUDE
    kv=LATITUDE LONGITUDE

## Running the Bot:
Ensure your environment variables are set correctly, then run the Telegram client:
    ```bash
    python tg_weather.py

## Usage
Start the bot in Telegram using the /start command.
Use the inline buttons to select the location and the time range (Current, Daily, or Weekly).
