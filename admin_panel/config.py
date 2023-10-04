'''Файл загружает переменные из окружения'''

import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env

BASE = os.path.dirname(os.path.abspath(__file__))

project = {
    'base': BASE,
    'log': BASE + os.getenv('LOGGING_PATH')
}

database = {
    'host': os.getenv('DATABASE_HOST'),
    'port': os.getenv('DATABASE_PORT'),
    'user': os.getenv('DATABASE_USER'),
    'password': os.getenv('DATABASE_PASSWORD'),
}

server = {
    'host': os.getenv('SERVER_HOST'),
    'port': os.getenv('SERVER_PORT'),
    'secret_key': os.getenv('SERVER_SECRET_KEY')
}
