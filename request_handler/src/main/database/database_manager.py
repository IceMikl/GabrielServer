import time

from request_handler.src.main.config import config

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from request_handler.src.main.datasources.datasource_manager import DatasourceManager


class DatabaseManager:

    __instance = None

    @staticmethod
    def get_instance():
        if DatabaseManager.__instance == None:
            DatabaseManager()
        return DatabaseManager.__instance


    def __init__(self):
        if DatabaseManager.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            self.connect_to_database()
            self.datasource_manager = DatasourceManager()
            DatabaseManager.__instance = self


    def create_db_session(self):
        return Session(bind=self.engine)


    def connect_to_database(self, attempt=0):
        self.engine = None
        try:
            self.engine = create_engine(config.DB_CONNECTION_URI, executemany_mode='values')
            print("[INFO] Connection to Postgres database was established successfully!")
        except Exception as e:
            print(f'[INFO] Retry to connect in 5 seconds, attempt # {attempt}, \n An exception occurred: {e} \n')
            time.sleep(5.0)
            attempt += 1
            self.connect_to_database(attempt)



