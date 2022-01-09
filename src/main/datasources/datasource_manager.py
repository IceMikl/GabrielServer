
from src.main.datasources.bna_blocked_numbers import BNABlockedNumbers
from src.main.datasources.bna_given_numbers import BNAGivenNumbers
from src.main.datasources.tellows_api import TellowsAPI

class DatasourceManager:

    def __init__(self):
        pass


    def get_data_from_bundesnetzagentur_blocked_numbers(self, do_scraping):
        bna_block_numbers = BNABlockedNumbers()
        return bna_block_numbers.get_latest_data(do_scraping)


    def get_data_from_bundesnetzagentur_given_numbers(self, parse_csv_file):
        bna_given_numbers = BNAGivenNumbers()
        return bna_given_numbers.parse_given_number_blocks(parse_csv_file=parse_csv_file)


    def get_tellows_actual_black_list(self, make_request=False):
        tellowsApi = TellowsAPI()
        return tellowsApi.get_actual_black_list(make_request=make_request)
