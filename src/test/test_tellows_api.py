
from src.main.datasources.tellows_api import TellowsAPI


def test_phone_number(phone_number='07812-1968053101'):
    tellows_api = TellowsAPI()
    tellows_api.test_phone_number(phone_number=phone_number)


def test_reading_actual_black_list():
    tellows_api = TellowsAPI()
    tellows_api.get_actual_black_list()



if __name__ == '__main__':
    #test_phone_number(phone_number='07812-1968053101')
    test_reading_actual_black_list()