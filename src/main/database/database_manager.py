import os
import re
import time
import logging as logger

from src.main.config import config

from sqlalchemy import create_engine, and_
from sqlalchemy.orm import Session

import src.main.database.models as db_models
from src.main.database.models import BlockedNumber

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
            self.connect_to_database()
            self.initialize_db_models()
            self.datasource_manager = DatasourceManager()
            DatabaseManager.__instance = self


    def create_db_session(self):
        return Session(bind=self.engine)


    def connect_to_database(self, attempt=0):
        self.engine = None
        try:
            self.engine = create_engine(config.DB_CONNECTION_URI, executemany_mode='values')
            print("[INFO] Connection to Postgres database was established successfully!")
        except Exception as e:
            print(f'[INFO] Retry to connect in 5 seconds, attempt # {attempt}')
            time.sleep(5.0)
            attempt += 1
            self.connect_to_database(attempt)



    def initialize_db_models(self):
        db_models.BaseModel.BASE.metadata.create_all(self.engine)


    def add_bna_blocked_numbers(self, do_scaping):
        counter = 0
        actual_data = self.datasource_manager.get_data_from_bundesnetzagentur_blocked_numbers(do_scaping)
        start_time = time.time()
        for json_number_object in actual_data:
            if("numbers_list" in json_number_object.keys()):
                for number in json_number_object["numbers_list"]:
                    if(self.is_phone_number(number)):
                        description = f'Bundesnetzagentur hat diese Nummer blockiert, {json_number_object["category"]}'
                        self.put_number(phone_number=number, description=description, suspicious=9)
                        counter += 1
        print(f'[INFO] {counter} blocked numbers from Bundesnetzagentur were added to database in {time.time() - start_time} seconds')


    def put_number(self, phone_number, description, suspicious):
        db_session = self.create_db_session()
        blocked_number = db_session.query(BlockedNumber).filter_by(phone_number=phone_number).first()
        if(blocked_number == None):
            new_blocked_number = db_models.BlockedNumber(phone_number=phone_number, description=description, suspicious=suspicious)
            db_session.add(new_blocked_number)
        else:
            blocked_number.description = description
            blocked_number.suspicious = suspicious
        db_session.commit()



    def is_phone_number(self, value):
        pattern = re.compile("(\+)?[0-9]+")
        return pattern.match(str(value))



    def add_bundesnetzagentur_given_numbers(self, parse_csv_file):
        start_time = time.time()
        given_numbers = self.datasource_manager.get_data_from_bundesnetzagentur_given_numbers(parse_csv_file=parse_csv_file)
        for number_block_json in given_numbers:
            self.put_number_block(number_block_json=number_block_json)
        print(f'[INFO] Given number block from Bundesnetzagentur were added to database in {time.time() - start_time} seconds')


    def put_number_block(self, number_block_json):
        start_time = time.time()
        db_session = self.create_db_session()
        number_blocks_to_add = []

        area_code = int(number_block_json['area_code'])
        phone_block_from = int(number_block_json['phone_block_from'])
        phone_block_to = int(number_block_json['phone_block_to'])
        phone_provider = number_block_json['phone_provider']
        place_name = number_block_json['place_name']

        given_number_block = db_session.query(db_models.GivenNumberBlock).filter(
            and_(db_models.GivenNumberBlock.phone_block_from == phone_block_from,
                 db_models.GivenNumberBlock.phone_block_to == phone_block_to)
        ).first()
        if(given_number_block == None):
            new_given_number_block = db_models.GivenNumberBlock(
                area_code=area_code, phone_provider=phone_provider,
                place_name=place_name, phone_block_from=phone_block_from,
                phone_block_to=phone_block_to)
            number_blocks_to_add.append(new_given_number_block)
        db_session.add_all(number_blocks_to_add)
        db_session.commit()
        db_session.close()





