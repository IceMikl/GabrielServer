import re
import time

from db_manager.src.main.config import config

from sqlalchemy import create_engine, and_
from sqlalchemy.orm import Session

import db_manager.src.main.database.models as db_models
from db_manager.src.main.database.models import BlockedNumber, TellowsNumber, GivenNumberBlock, AreaCode

from db_manager.src.main.datasources.datasource_manager import DatasourceManager


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
            print(f'[INFO] Retry to connect in 5 seconds, attempt # {attempt}, \n An exception occurred: {e} \n')
            time.sleep(5.0)
            attempt += 1
            self.connect_to_database(attempt)



    def initialize_db_models(self):
        db_models.BaseModel.BASE.metadata.create_all(self.engine)


    def add_bna_blocked_numbers(self, do_scraping):
        counter = 0
        actual_data = self.datasource_manager.get_data_from_bundesnetzagentur_blocked_numbers(do_scraping)
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
            new_blocked_number = BlockedNumber(phone_number=phone_number, description=description, suspicious=suspicious)
            db_session.add(new_blocked_number)
        else:
            blocked_number.description = description
            blocked_number.suspicious = suspicious
        db_session.commit()



    def is_phone_number(self, value):
        pattern = re.compile("(\+)?[0-9]+")
        return pattern.match(str(value))



    def add_bundesnetzagentur_given_numbers(self, parse_csv_file, deploy_mode):
        start_time = time.time()
        given_numbers = self.datasource_manager.get_data_from_bundesnetzagentur_given_numbers(parse_csv_file=parse_csv_file,
                                                                                              deploy_mode=deploy_mode)
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

        given_number_block = db_session.query(GivenNumberBlock).filter(
            and_(GivenNumberBlock.phone_block_from == phone_block_from,
                 GivenNumberBlock.phone_block_to == phone_block_to)
        ).first()
        if(given_number_block == None):
            new_given_number_block = GivenNumberBlock(
                area_code=area_code, phone_provider=phone_provider,
                place_name=place_name, phone_block_from=phone_block_from,
                phone_block_to=phone_block_to)
            number_blocks_to_add.append(new_given_number_block)
        db_session.add_all(number_blocks_to_add)
        db_session.commit()
        db_session.close()





    def add_tellowsApi_actual_black_list(self, make_request=False):
        start_time = time.time()
        tellows_black_list = self.datasource_manager.get_tellows_actual_black_list(make_request=make_request)
        for number_json_block in tellows_black_list:
            self.put_tellows_number(number_json_block=number_json_block)
        print(f'[INFO] Tellows actual black list was added to database in {time.time() - start_time} seconds')


    def put_tellows_number(self, number_json_block):
        start_time = time.time()
        db_session = self.create_db_session()
        list_to_add = []

        number = number_json_block['number'] if 'number' in number_json_block else ''
        score = number_json_block['score'] if 'score' in number_json_block else 5
        complains = number_json_block['complains'] if 'complains' in number_json_block else 0
        country = number_json_block['country'] if 'country' in number_json_block else 0
        prefix = number_json_block['prefix'] if 'prefix' in number_json_block else 0
        searches = number_json_block['searches'] if 'searches' in number_json_block else 0
        caller_type = number_json_block['callertype'] if 'callertype' in number_json_block else ''
        caller_name = number_json_block['callername'] if 'callername' in number_json_block else ''
        last_comment = number_json_block['lastcomment'] if 'lastcomment' in number_json_block else ''
        deeplink = number_json_block['deeplink'] if 'deeplink' in number_json_block else ''
        caller_typeid = number_json_block['callertypeid'] if 'callertypeid' in number_json_block else 0

        tellows_number = db_session.query(TellowsNumber).filter(TellowsNumber.number==number).first()
        if(tellows_number == None):
            new_given_number_block = TellowsNumber(
                number=number, score = score, complains = complains, country = country, prefix = prefix,
                searches = searches, caller_type = caller_type, caller_name = caller_name,
                last_comment = last_comment, deeplink = deeplink, caller_typeid = caller_typeid)
            list_to_add.append(new_given_number_block)
        db_session.add_all(list_to_add)
        db_session.commit()
        db_session.close()



    def add_germany_area_codes(self, parse_csv_file=False):
        start_time = time.time()
        area_codes = self.datasource_manager.get_bna_germany_area_codes(parse_csv_file=parse_csv_file)
        for area_code in area_codes:
            self.put_area_code(area_code_json=area_code)
        print(
            f'[INFO] Given Bundesnetzagentur Germany area codes were added to database in {time.time() - start_time} seconds')



    def put_area_code(self, area_code_json):
        start_time = time.time()
        db_session = self.create_db_session()
        area_codes_to_add = []

        area_code = int(area_code_json['area_code'])
        place_name = area_code_json['place_name']
        activ = int(area_code_json['activ'])
        country = area_code_json['country']

        area_code_object = db_session.query(AreaCode).filter(
            AreaCode.code == area_code
        ).first()
        if(area_code_object == None):
            new_area_code = AreaCode(code=area_code, place_name=place_name, activ=activ, country=country)
            area_codes_to_add.append(new_area_code)
        db_session.add_all(area_codes_to_add)
        db_session.commit()
        db_session.close()