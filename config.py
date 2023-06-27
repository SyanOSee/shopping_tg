'''Файл загружает переменные из окружения'''

import os

from dotenv import load_dotenv

load_dotenv()

# Spam limitation
SPAM_RATE = 1

# Telegram Bot Token
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Database <Postgresql>
DATABASE_HOST = os.getenv("DATABASE_HOST")
DATABASE_PORT = os.getenv("DATABASE_PORT")
DATABASE_USER = os.getenv("DATABASE_USER")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")

# Project directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Database <Sqlite>
DATABASE_PATH = BASE_DIR + os.getenv("DATABASE_PATH")

# Log file path
LOGGING_PATH = BASE_DIR + os.getenv("LOGGING_PATH")

# Flask secret key
SERVER_SECRET_KEY = os.getenv("SERVER_SECRET_KEY")

# Webhook [Optional]
NGROK_URL = 'https://5131-85-115-248-151.ngrok-free.app' # For testing webhook locally
BASE_URL = '127.0.0.1'
WEBHOOK_PATH = os.getenv("WEBHOOK_PATH")

# Payment tokens
SBERBANK = os.getenv('SBERBANK')
UKASSA = os.getenv('UKASSA')
