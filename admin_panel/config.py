import os
from dotenv import load_dotenv

load_dotenv()

# Database
DATABASE_HOST = os.getenv('DATABASE_HOST')
DATABASE_PORT = os.getenv('DATABASE_PORT')
DATABASE_USER = os.getenv('DATABASE_USER')
DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD')
DATABASE_PATH = os.getenv('DATABASE_PATH')

# Server
SERVER_HOST = os.getenv('SERVER_HOST')
SERVER_PORT = os.getenv('SERVER_PORT')
SERVER_SECRET_KEY = os.getenv('SERVER_SECRET_KEY')

# Logging
LOGGING_PATH = os.getenv('LOGGING_PATH')