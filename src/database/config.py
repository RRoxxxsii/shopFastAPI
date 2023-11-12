import os

from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.environ.get('SECRET_KEY')

# Main DB Settings
DB_USER = os.environ.get('POSTGRES_USER')
DB_PASS = os.environ.get('POSTGRES_PASSWORD')
DB_NAME = os.environ.get('POSTGRES_DB')
DB_HOST = os.environ.get('POSTGRES_HOST')
DB_PORT = os.environ.get('POSTGRES_PORT')

# Test DB Settings
POSTGRES_USER_TEST = os.environ.get('POSTGRES_USER_TEST')
POSTGRES_PASSWORD_TEST = os.environ.get('POSTGRES_PASSWORD_TEST')
POSTGRES_DB_TEST = os.environ.get('POSTGRES_DB_TEST')
POSTGRES_HOST_TEST = os.environ.get('POSTGRES_HOST_TEST')
POSTGRES_PORT_TEST = os.environ.get('POSTGRES_PORT_TEST')
