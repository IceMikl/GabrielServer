import sys

if("/" not in sys.path):
    sys.path.append("/")
print(sys.path)

import datetime

from flasgger import Swagger

from flask import Flask, request
from flask_basicauth import BasicAuth

import db_manager.src.main.config.config as config
import db_manager.src.main.database.database_manager as db_manager
from db_manager.src.main.database.models import BlockedNumber, GivenNumberBlock, TellowsNumber, AreaCode,  Request



class Server:

    swagger_template = {
        "swagger": "2.0",
        "info": {
            "title": "Gabriel Server API",
            "description": "API for Gabriel server",
            "contact": {
                "responsibleOrganization": "Gabriel",
                "responsibleDeveloper": "Gabriel team",
                "email": "info@gabriel-schutz.de",
                "url": "https://gabriel-schutz.de/#",
            },
            "termsOfService": "https://gabriel-schutz.de/impressum",
            "version": "0.0.1"
        },
        "host": "mysite.com",  # overrides localhost:500
        "basePath": "/apidocs",  # base bash for blueprint registration
        "schemes": [
            "http",
            "https"
        ],
        "operationId": "getmyData"
    }

    app = Flask(__name__)
    swagger = Swagger(app, template=swagger_template)


    def __init__(self):
        self.initialize()


    def initialize(self):
        self.app.config['BASIC_AUTH_USERNAME'] = config.BASIC_AUTH_USERNAME
        self.app.config['BASIC_AUTH_PASSWORD'] = config.BASIC_AUTH_PASSWORD
        self.app.config['BASIC_AUTH_FORCE'] = config.BASIC_AUTH_FORCE
        BasicAuth(self.app)


    def start(self, develop_mode=False):
        self.create_database(do_scraping=False, parse_csv_file=False, develop_mode=develop_mode)
        self.app.run(debug=True, use_reloader=False, port=8087, host="0.0.0.0")


    def create_database(self, do_scraping=False, parse_csv_file=True, develop_mode=False):
        database_manager = db_manager.DatabaseManager()
        database_manager.add_bna_blocked_numbers(do_scraping=do_scraping)
        database_manager.add_bundesnetzagentur_given_numbers(parse_csv_file=parse_csv_file, develop_mode=develop_mode)
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
        return f'Exceed number of requests: {get_number_of_requests()}', 403


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

