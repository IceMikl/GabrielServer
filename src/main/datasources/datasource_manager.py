
from src.main.datasources.bna_blocked_numbers import BNABlockedNumbers
from src.main.datasources.bna_given_numbers import BNAGivenNumbers

class DatasourceManager:

    def __init__(self):
        pass


    def get_data_from_bundesnetzagentur_blocked_numbers(self, do_scaping):
        bna_block_numbers = BNABlockedNumbers()
        return bna_block_numbers.get_latest_data(do_scaping)


    def get_data_from_bundesnetzagentur_given_numbers(self, parse_given_numbers_csv):
        bna_given_numbers = BNAGivenNumbers()
        return bna_given_numbers.get_given_number_blocks(parse_given_numbers_csv)

