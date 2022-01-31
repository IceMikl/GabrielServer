import sys

if("/" not in sys.path):
    sys.path.append("/")
print(sys.path)

import datetime

from flasgger import Swagger

from flask import Flask, request
from flask_basicauth import BasicAuth

import request_handler.src.main.database.database_manager as db_manager
from request_handler.src.main.database.models import Request

# Blueprints
from request_handler.src.main.server.request_handlers.phone_numbers_handler import numbers
from request_handler.src.main.server.request_handlers.news_handler import news
from request_handler.src.main.server.request_handlers.area_codes_handler import area_codes




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
        self.app.register_blueprint(numbers, url_prefix='/api/numbers/')
        self.app.register_blueprint(news, url_prefix='/api/news/')
        self.app.register_blueprint(area_codes, url_prefix='/api/area_codes/')

        self.app.config['BASIC_AUTH_USERNAME'] = 'user'
        self.app.config['BASIC_AUTH_PASSWORD'] = 'gabriel_user'
        self.app.config['BASIC_AUTH_FORCE'] = True
        BasicAuth(self.app)


    def start(self):
        self.app.run(debug=True, use_reloader=False, port=8080, host="0.0.0.0")




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

