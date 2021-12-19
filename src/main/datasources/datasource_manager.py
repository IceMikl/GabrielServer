
from src.main.datasources.bundesnetzagentur import Bundesnetzagentur

class DatasourceManager:

    def __init__(self):
        pass


    def scrap_data_from_bundesnetzagentur(self):
        bundesnetzagentur = Bundesnetzagentur()
        return bundesnetzagentur.get_actual_data()