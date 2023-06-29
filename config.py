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
APP_HOST = os.getenv('APP_HOST')
APP_PORT = os.getenv('APP_PORT')
WEBHOOK_URL = os.getenv('WEBHOOK_URL')
SERVER_SECRET_KEY = os.getenv("SERVER_SECRET_KEY")
WEBHOOK_PATH = os.getenv("WEBHOOK_PATH") + '/' + BOT_TOKEN

# Log file path
LOGGING_PATH = BASE_DIR + os.getenv("LOGGING_PATH")

# Payment tokens
SBERBANK = os.getenv('SBERBANK')
UKASSA = os.getenv('UKASSA')
