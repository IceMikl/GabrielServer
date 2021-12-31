
from src.main.datasources.tellows_api import TellowsAPI



if __name__ == '__main__':

    tellows_api = TellowsAPI()
    tellows_api.test_phone_number()
    tellows_api.get_actual_black_list()