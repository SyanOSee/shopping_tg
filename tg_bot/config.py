'''Файл загружает переменные из окружения'''

import os
from dotenv import load_dotenv


load_dotenv()  # Load environment variables from .env

BASE = os.path.dirname(os.path.abspath(__file__))

project = {
    'base': BASE,
    'log': BASE + os.getenv('LOGGING_PATH')
}

bot = {
    'token': os.getenv('BOT_TOKEN'),  # Telegram tg_bot token
    'spam_rate': 1  # Spamming interval in seconds
}

payment = {
    'ukassa': os.getenv('UKASSA')
}

database = {
    'host': os.getenv('DATABASE_HOST'),
    'port': os.getenv('DATABASE_PORT'),
    'user': os.getenv('DATABASE_USER'),
    'password': os.getenv('DATABASE_PASSWORD'),
}

server = {
    'url': os.getenv('SERVER_URL')
}