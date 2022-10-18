'''Файл загружает переменные из окружения'''

import os

from dotenv import load_dotenv

load_dotenv()

# Telegram Bot Token
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Database <Postgresql>
DATABASE_HOST = os.getenv("DATABASE_HOST")
DATABASE_PORT = os.getenv("DATABASE_PORT")
DATABASE_USER = os.getenv("DATABASE_USER")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")

# Database <Sqlite>
DATABASE_PATH = os.getenv("DATABASE_PATH")

# Log file path
LOGGING_PATH = os.getenv("LOGGING_PATH")

# Webhook [Optional]
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
WEBHOOK_PATH = "/bot/" + BOT_TOKEN

# Chrome Driver <Selenium> [Optional]
CHROME_DRIVER_VERSION = os.getenv("CHROME_DRIVER_VERSION")

# Qiwi Tokens [Optional]
QIWI_PUBLIC_TOKEN = os.getenv("QIWI_PUBLIC_TOKEN")
QIWI_SECRET_TOKEN = os.getenv("QIWI_SECRET_TOKEN")