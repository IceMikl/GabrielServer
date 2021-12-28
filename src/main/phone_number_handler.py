
import phonenumbers
from phonenumbers import carrier, timezone, geocoder


class PhoneNumberHandler:


    @staticmethod
    def analyze_number(phone_number):
        phone_number_information = {}
        parsed_number = phonenumbers.parse(phone_number, "DE")
        phone_number_information['original_number'] = phone_number
        print("parsed_number: " + str(parsed_number))
        if(phonenumbers.is_valid_number(parsed_number)):
            phone_number_information['valid'] = True
            phone_number_information['country_code'] = parsed_number.country_code
        else:
            phone_number_information['valid'] = False
        return phone_number_information