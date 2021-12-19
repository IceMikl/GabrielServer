
import re
import time
import logging as logger

import src.main.database.models as db_models
print("import src.main.app as app")
#import src.main.app as app
from src.main.datasources.datasource_manager import DatasourceManager


class DatabaseManager:

    def __init__(self, database):
        self.database = database
        self.datasource_manager = DatasourceManager()


    def add_data_from_bundesnetzagentur(self):
        actual_data = self.datasource_manager.scrap_data_from_bundesnetzagentur()
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


    def put_number(self, phone_number, description, suspicious):
        number = db_models.NumberModel.query.filter_by(phone_number=phone_number).first()
        if not number:
            new_number = db_models.NumberModel(phone_number=phone_number, description=description, suspicious=suspicious)
            self.database.session.add(new_number)
        else:
            number.description = description
            number.suspicious = suspicious
        self.database.session.commit()


    def is_number(self, value):
        pattern = re.compile("(\+)?[0-9]+")
        return pattern.match(value)
