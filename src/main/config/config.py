
import os

os.environ['POSTGRES_USER'] = 'admin'
os.environ['POSTGRES_PASSWORD'] = 'password'
os.environ['POSTGRES_HOST'] = 'postgres_db'
os.environ['POSTGRES_DB'] = '5678'
os.environ['POSTGRES_PORT'] = 'database'

user = os.environ['POSTGRES_USER']
password = os.environ['POSTGRES_PASSWORD']
host = os.environ['POSTGRES_HOST']
database = os.environ['POSTGRES_DB']
port = os.environ['POSTGRES_PORT']

#DB_CONNECTION_URI = f'postresql://{user}:{password}@{host}:{port}/{database}'
DB_CONNECTION_URI = 'sqlite:///database.db'