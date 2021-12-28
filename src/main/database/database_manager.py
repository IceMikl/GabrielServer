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


    def initialize_db_models(self):
        db_models.BaseModel.BASE.metadata.create_all(self.engine)


    def add_bna_blocked_numbers(self, do_scaping):
        actual_data = self.datasource_manager.get_data_from_bundesnetzagentur_blocked_numbers(do_scaping)
        start_time = time.time()
        for json_number_object in actual_data:
            if("numbers_list" in json_number_object.keys()):
                for number in json_number_object["numbers_list"]:
                    if(self.is_phone_number(number)):
                        description = f'Bundesnetzagentur hat diese Nummer blockiert, {json_number_object["category"]}'
                        self.put_number(phone_number=number, description=description, suspicious=9)
                    else:
                        print(f'not number format: {number}, date: {json_number_object["date"]}')
        logger.info(f'Data from Bundesnetzagentur were added to database in {time.time() - start_time} seconds')


    def put_number(self, phone_number, description, suspicious):
        db_session = self.create_db_session()
        blocked_number = db_session.query(BlockedNumber).filter_by(phone_number=phone_number).first()
        if not blocked_number:
            new_blocked_number = db_models.BlockedNumber(phone_number=phone_number, description=description, suspicious=suspicious)
            db_session.add(new_blocked_number)
        else:
            blocked_number.description = description
            blocked_number.suspicious = suspicious
        db_session.commit()



    def is_phone_number(self, value):
        pattern = re.compile("(\+)?[0-9]+")
        return pattern.match(str(value))



    def add_bundesnetzagentur_given_numbers(self, parse_given_numbers_csv):
        pass
        '''
        start_time = time.time()
        given_numbers = self.datasource_manager.get_data_from_bundesnetzagentur_given_numbers(parse_given_numbers_csv)
        for number_block in given_numbers:
            self.put_block(area_code=number_block['area_code'], place_name=number_block['place_name'],
                           phone_block_from=number_block['phone_block_from'], phone_block_to=number_block['area_code'],
                           block_size=number_block['block_size'], phone_provider=number_block['phone_provider'])
        logger.info(f'Given number from Bundesnetzagentur were added to database in {time.time() - start_time} seconds')

    def put_block(self, area_code, place_name, phone_block_from, phone_block_to, block_size, phone_provider):
        generated_id = self.generate_id(area_code=area_code, place_name=place_name, phone_block_from=phone_block_from,
                                        phone_block_to=phone_block_to, phone_provider=phone_provider)
        number_block = app.NumberBlock.query.filter_by(id=generated_id).first()
        if not number_block:
            new_number_block = app.NumberBlock(id=generated_id, area_code=area_code, place_name=place_name,
                                               phone_block_from=phone_block_from, phone_block_to=phone_block_to,
                                               block_size=block_size, phone_provider=phone_provider)
            self.database.session.add(new_number_block)
        else:
            number_block.area_code = area_code
            number_block.place_name = place_name
            number_block.phone_block_from = phone_block_from
            number_block.phone_block_from = phone_block_from
            number_block.phone_block_to = phone_block_to
            number_block.block_size = block_size
            number_block.phone_provider = phone_provider
        self.database.session.commit()
        
    
    def generate_id(self, area_code, place_name, phone_block_from, phone_block_to, phone_provider):
        return str(hash(str(f'{area_code}_{place_name}_{phone_block_from}_{phone_block_to}_{phone_provider}')))
        
    '''

