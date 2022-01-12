
from src.main.phone_number_parser import PhoneNumberHandler



def parse_test_numbers():
    phone_number_handler = PhoneNumberHandler()
    print(phone_number_handler.analyze_number('02016489000'))
    print(phone_number_handler.analyze_number('+492016489000'))



if __name__ == '__main__':
    parse_test_numbers()
