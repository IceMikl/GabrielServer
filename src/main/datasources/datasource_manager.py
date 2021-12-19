
from src.main.datasources.bna_blocked_numbers import BNABlockedNumbers
from src.main.datasources.bna_given_numbers import BNAGivenNumbers

class DatasourceManager:

    def __init__(self):
        pass


    def get_data_from_bundesnetzagentur_blocked_numbers(self):
        bna_block_numbers = BNABlockedNumbers()
        return bna_block_numbers.get_latest_data()


    def get_data_from_bundesnetzagentur_given_numbers(self):
        bna_given_numbers = BNAGivenNumbers()
        return bna_given_numbers.get_given_number_blocks()


if __name__ == "__main__":
    datasource_manager = DatasourceManager()
    datasource_manager.get_data_from_bundesnetzagentur_given_numbers()