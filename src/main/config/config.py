
import os

os.environ['POSTGRES_DB'] = 'database'
os.environ['POSTGRES_USER'] = 'admin'
os.environ['POSTGRES_PASSWORD'] = 'password'
os.environ['POSTGRES_HOST'] = 'localhost'
os.environ['POSTGRES_PORT'] = '5432'

database = os.environ['POSTGRES_DB']
user = os.environ['POSTGRES_USER']
password = os.environ['POSTGRES_PASSWORD']
host = os.environ['POSTGRES_HOST']
port = os.environ['POSTGRES_PORT']

DB_CONNECTION_URI = f'postgresql://{user}:{password}@{host}:{port}/{database}'
print(f"DB_CONNECTION_URI: {DB_CONNECTION_URI}")
#DB_CONNECTION_URI = 'sqlite:///database.db'