import os

os.environ["POSTGRES_USER"] = 'admin'
os.environ["POSTGRES_PASSWORD"] = 'password'
os.environ["POSTGRES_HOST"] = 'localhost'
os.environ["POSTGRES_PORT"] = '5432'
os.environ["POSTGRES_DB"] = 'postgres_db'

POSTGRES_USER = os.environ["POSTGRES_USER"]
POSTGRES_PASSWORD = os.environ["POSTGRES_PASSWORD"]
POSTGRES_HOST = os.environ["POSTGRES_HOST"]
POSTGRES_PORT = os.environ["POSTGRES_PORT"]
POSTGRES_DB = os.environ["POSTGRES_DB"]

DB_CONNECTION_URI = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'

PATH_TO_RESOURCES_FOLDER = os.path.dirname(os.path.abspath(__file__)) + '/../../../resources/'
