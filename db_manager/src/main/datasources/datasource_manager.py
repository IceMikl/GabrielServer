
from db_manager.src.main.datasources.numbers.bna_blocked_numbers import BNABlockedNumbers
from db_manager.src.main.datasources.numbers.bna_given_numbers import BNAGivenNumbers
from db_manager.src.main.datasources.numbers.tellows_api import TellowsAPI
from db_manager.src.main.datasources.news.sueddeutsche_news_api import SueddeutscheNewsApi
from db_manager.src.main.datasources.news.faz_news_api import FazNewsApi
from db_manager.src.main.datasources.area_codes.bna_germany_area_codes import BNAGermanyAreaCodes


class DatasourceManager:

    def __init__(self):
        pass


    def get_data_from_bundesnetzagentur_blocked_numbers(self, do_scraping):
        bna_block_numbers = BNABlockedNumbers()
        return bna_block_numbers.get_latest_data(do_scraping)


    def get_data_from_bundesnetzagentur_given_numbers(self, parse_csv_file, develop_mode):
        bna_given_numbers = BNAGivenNumbers()
        return bna_given_numbers.parse_given_number_blocks(parse_csv_file=parse_csv_file, develop_mode=develop_mode)


    def get_tellows_actual_black_list(self, make_request=False):
        tellowsApi = TellowsAPI()
        return tellowsApi.get_actual_black_list(make_request=make_request)


    def get_sueddeutsche_news(self, make_request=False):
        sueddeusche_news = SueddeutscheNewsApi()
        return sueddeusche_news.get_news(make_request=make_request)


    def get_faz_news(self, make_request=False):
        faz_news = FazNewsApi()
        return faz_news.get_news(make_request=make_request)


    def get_bna_germany_area_codes(self, parse_csv_file=False):
        bna_germany_area_codes = BNAGermanyAreaCodes()
        return bna_germany_area_codes.get_area_codes(parse_csv_file=parse_csv_file)