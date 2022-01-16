import sys

if("/" not in sys.path):
    sys.path.append("/")
print(sys.path)


from flask import Flask
from flask_basicauth import BasicAuth

import src.main.database.database_manager as db_manager
from src.main.database.models import BlockedNumber, GivenNumberBlock, TellowsNumber, AreaCode

# Blueprints
from src.main.server.request_handlers.phone_numbers_handler import numbers
from src.main.server.request_handlers.news_handler import news
from src.main.server.request_handlers.area_codes_handler import area_codes


class Server:

    def __init__(self):
        self.initialize()



    def initialize(self):
        self.app = Flask(__name__)
        self.app.register_blueprint(numbers, url_prefix='/api/numbers/')
        self.app.register_blueprint(news, url_prefix='/api/news/')
        self.app.register_blueprint(area_codes, url_prefix='/api/area_codes/')

        self.app.config['BASIC_AUTH_USERNAME'] = 'user'
        self.app.config['BASIC_AUTH_PASSWORD'] = 'gabriel_user'
        self.app.config['BASIC_AUTH_FORCE'] = True
        basic_auth = BasicAuth(self.app)


    def start(self):
        self.create_database(do_scraping=False, parse_csv_file=False)
        self.app.run(debug=True, use_reloader=False, port=8080, host="0.0.0.0")


    def create_database(self, do_scraping=False, parse_csv_file=True):
        database_manager = db_manager.DatabaseManager()
        database_manager.add_bna_blocked_numbers(do_scraping=do_scraping)
        database_manager.add_bundesnetzagentur_given_numbers(parse_csv_file=parse_csv_file)
        database_manager.add_tellowsApi_actual_black_list(make_request=False)
        database_manager.add_germany_area_codes(parse_csv_file=True)
        self.test_database()


    def test_database(self):
        database_manager = db_manager.DatabaseManager.get_instance()
        db_session = database_manager.create_db_session()
        print(db_session.query(BlockedNumber).limit(20).all())
        print(db_session.query(GivenNumberBlock).limit(20).all())
        print(db_session.query(TellowsNumber).limit(20).all())
        print(db_session.query(AreaCode).limit(20).all())
        db_session.close()

