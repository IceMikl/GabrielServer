import sys

if("/" not in sys.path):
    sys.path.append("/")
print(sys.path)

from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

import src.main.database.database_manager as db_manager

from config import config

import psycopg2

try:
    conn = psycopg2.connect(
        "dbname='template1'"
        " user='dbuser'"
        " host='localhost'"
        " password='dbpass'")
except:
    print("I am unable to connect to the database")


app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = config.DB_CONNECTION_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

import src.main.resource_handlers.number_resource_handler as number_resource_handler
api.add_resource(number_resource_handler.NumberResourceHandler, "/api/number/<string:phone_number>")


def initialize_database():
    print("initialize_database")
    db.drop_all()
    db.create_all()
    add_data_to_database()


def add_data_to_database():
    database_manager = db_manager.DatabaseManager(database=db)
    database_manager.add_data_from_bundesnetzagentur()


if __name__ == "__main__":
    initialize_database()
    app.run(debug=True, use_reloader=False, port=8080, host="0.0.0.0")

