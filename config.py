'''Файл загружает переменные из окружения'''

import os

from dotenv import load_dotenv

load_dotenv()

# Spam limitation
SPAM_RATE = 1

# Telegram Bot Token
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Project directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Database
DATABASE_HOST = os.getenv("DATABASE_HOST")
DATABASE_PORT = os.getenv("DATABASE_PORT")
DATABASE_USER = os.getenv("DATABASE_USER")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
DATABASE_PATH = BASE_DIR + os.getenv("DATABASE_PATH")

# Server
ADMIN_PANEL_HOST = os.getenv('ADMIN_PANEL_HOST')
ADMIN_PANEL_PORT = os.getenv('ADMIN_PANEL_PORT')
BASE_URL = '127.0.0.1'
WEBHOOK_PATH = os.getenv("WEBHOOK_PATH")
SERVER_SECRET_KEY = os.getenv("SERVER_SECRET_KEY")

# Log file path
LOGGING_PATH = BASE_DIR + os.getenv("LOGGING_PATH")

# Payment tokens
SBERBANK = os.getenv('SBERBANK')
UKASSA = os.getenv('UKASSA')
