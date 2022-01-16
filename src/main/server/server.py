import sys

if("/" not in sys.path):
    sys.path.append("/")
print(sys.path)

import datetime

from flask import Flask, request
from flask_basicauth import BasicAuth

import src.main.database.database_manager as db_manager
from src.main.database.models import BlockedNumber, GivenNumberBlock, TellowsNumber, AreaCode, Request

# Blueprints
from src.main.server.request_handlers.phone_numbers_handler import numbers
from src.main.server.request_handlers.news_handler import news
from src.main.server.request_handlers.area_codes_handler import area_codes




class Server:


    app = Flask(__name__)

    def __init__(self):
        self.initialize()


    def initialize(self):

        self.app.register_blueprint(numbers, url_prefix='/api/numbers/')
        self.app.register_blueprint(news, url_prefix='/api/news/')
        self.app.register_blueprint(area_codes, url_prefix='/api/area_codes/')

        self.app.config['BASIC_AUTH_USERNAME'] = 'user'
        self.app.config['BASIC_AUTH_PASSWORD'] = 'gabriel_user'
        self.app.config['BASIC_AUTH_FORCE'] = True
        BasicAuth(self.app)


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



app = Server.app
@app.before_request
def before_each_request():
    add_request()
    if get_number_of_requests() > 100:
        return 'Exceed number of requests', 403




def add_request():
    new_request = Request(remote_addr=str(request.remote_addr), base_url=str(request.base_url),
                          content_encoding=str(request.content_encoding), content_type=str(request.content_type),
                          date=str(request.date), data=str(request.data), full_path=str(request.full_path),
                          headers=str(request.headers),
                          host=str(request.host), host_url=str(request.host_url), path=str(request.path),
                          remote_user=str(request.remote_user), scheme=str(request.scheme), url=str(request.url),
                          url_charset=str(request.url_charset), url_root=str(request.url_root),
                          url_rule=str(request.url_rule),
                          user_agent=str(request.user_agent), request_time=datetime.datetime.now())

    database_manager = db_manager.DatabaseManager.get_instance()
    db_session = database_manager.create_db_session()
    db_session.add(new_request)
    db_session.commit()
    db_session.close()


def get_number_of_requests():
    remote_addr = str(request.remote_addr)
    database_manager = db_manager.DatabaseManager.get_instance()
    db_session = database_manager.create_db_session()
    number_of_requests = db_session.query(Request).filter_by(remote_addr=remote_addr).count()
    db_session.commit()
    db_session.close()
    return number_of_requests

