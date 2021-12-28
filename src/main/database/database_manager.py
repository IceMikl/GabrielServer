import os
import re
import time
import logging as logger

from src.main.config import config
#from src.main.database.models import


import psycopg2
from psycopg2 import OperationalError

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

import src.main.database.models as db_models
from src.main.database.models import BlockedNumber
#print("import src.main.app as app")
#import src.main.app as app
from src.main.datasources.datasource_manager import DatasourceManager


class DatabaseManager:

    __instance = None

    @staticmethod
    def get_instance():
        if DatabaseManager.__instance == None:
            DatabaseManager()
        return DatabaseManager.__instance


    def __init__(self):
        if DatabaseManager.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            # self.establish_connection_to_db()
            self.connect_to_db_sqlalchemy()
            self.initialize_db_models()
            self.datasource_manager = DatasourceManager()
            DatabaseManager.__instance = self


    def create_db_session(self):
        return Session(bind=self.engine)


    def connect_to_db_sqlalchemy(self):
        self.engine = None
        try:
            self.engine = create_engine(config.DB_CONNECTION_URI)
            print("Connection to Postgres database was established successfully!")
        except Exception as e:
            print(f'The error during connection to db: {e}')


    def establish_connection_to_db(self):
        self.connection = None
        try:
            self.connection = psycopg2.connect(
                database=config.POSTGRES_DB,
                user=config.POSTGRES_USER,
                password=config.POSTGRES_PASSWORD,
                host=config.POSTGRES_HOST,
                port=config.POSTGRES_PORT,
            )
            print("Connection to Postgres database was established successfully!")
        except OperationalError as e:
            print(f'The error {e} occurred')


    def initialize_db_models(self):
        db_models.BaseModel.BASE.metadata.create_all(self.engine)


    def add_bna_blocked_numbers(self):
        pass
        '''
        actual_data = self.datasource_manager.get_data_from_bundesnetzagentur_blocked_numbers()
        print(actual_data)
        start_time = time.time()
        for json_number_object in actual_data:

            if("numbers_list" in json_number_object.keys()):
                for number in json_number_object["numbers_list"]:
                    if(self.is_number(number)):
                        description = f'Bundesnetzagentur hat diese Nummer blockiert, {json_number_object["category"]}'
                        self.put_number(phone_number=number, description=description, suspicious=9)
                    else:
                        print(f'not number format: {number}, date: {json_number_object["date"]}')
        logger.info(f'Data from Bundesnetzagentur were added to database in {time.time() - start_time}')
        '''


    def put_number(self, phone_number, description, suspicious):
        pass
        '''
        number = db_models.NumberModel.query.filter_by(phone_number=phone_number).first()
        if not number:
            new_number = db_models.NumberModel(phone_number=phone_number, description=description, suspicious=suspicious)
            self.database.session.add(new_number)
        else:
            number.description = description
            number.suspicious = suspicious
        self.database.session.commit()
        '''


    def is_number(self, value):
        pattern = re.compile("(\+)?[0-9]+")
        return pattern.match(value)


    def add_bna_given_numbers(self):
        pass #TODO: implement Bundesnetzagentur given number blocks