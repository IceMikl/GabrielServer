import os

import phonenumbers
import json
from request_handler.src.main.config import config


class PhoneNumberHandler:


    PHONE_AREA_CODES = []
    PATH_TO_JSON_FILE = config.PATH_TO_RESOURCES_FOLDER + 'phone_area_codes.json'

    def __init__(self):
        self.read_phone_area_codes()


    def read_phone_area_codes(self):
        with open(self.PATH_TO_JSON_FILE, 'r') as f:
            self.PHONE_AREA_CODES = json.load(f)
            f.close()


    def analyze_number(self, phone_number):
        phone_number_information = {}
        parsed_number = phonenumbers.parse(phone_number, "DE")
        phone_number_information['original_number'] = phone_number
        if(phonenumbers.is_valid_number(parsed_number)):
            national_number = parsed_number.national_number
            phone_number_information['valid'] = True
            phone_number_information['country_code'] = parsed_number.country_code
            phone_number_information['national_number'] = parsed_number.national_number
            phone_number_information['area_code'] = self.find_area_code(national_number)
            phone_number_information['place_name'] = self.find_place_name(national_number)
            phone_number_information['phone_provider'] = self.find_phone_provider(national_number)
        else:
            phone_number_information['valid'] = False
        return phone_number_information


    def find_area_code(self, national_number):
        national_number_str = str(national_number)
        for area_code_block in self.PHONE_AREA_CODES:
            if national_number_str.startswith(str(area_code_block['area_code'])):
                return area_code_block['area_code']
        return ''


    def find_place_name(self, national_number):
        national_number_str = str(national_number)
        for area_code_block in self.PHONE_AREA_CODES:
            if national_number_str.startswith(str(area_code_block['area_code'])):
                return area_code_block['place_name']
        return ''


    def find_phone_provider(self, national_number):
        national_number_str = str(national_number)
        for area_code_block in self.PHONE_AREA_CODES:
            if national_number_str.startswith(str(area_code_block['area_code'])):
                return area_code_block['phone_provider']
        return ''


