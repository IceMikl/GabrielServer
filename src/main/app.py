import sys

if("/" not in sys.path):
    sys.path.append("/")
print(sys.path)


from sqlalchemy import and_
from flask import Flask
from flask_basicauth import BasicAuth

from phone_number_parser import PhoneNumberHandler
import src.main.database.database_manager as db_manager
from src.main.database.models import BlockedNumber, GivenNumberBlock, TellowsNumber

# Blueprints
from src.main.server.request_handlers.phone_numbers_handler import phone_numbers

app = Flask(__name__)
app.register_blueprint(phone_numbers, url_prefix='/api/phone_numbers/')

app.config['BASIC_AUTH_USERNAME'] = 'user'
app.config['BASIC_AUTH_PASSWORD'] = 'gabriel_user'
app.config['BASIC_AUTH_FORCE'] = True
basic_auth = BasicAuth(app)


def start_server():
    create_database(do_scraping=False, parse_csv_file=False)
    app.run(debug=True, use_reloader=False, port=8080, host="0.0.0.0")


def create_database(do_scraping=False, parse_csv_file=True):
    database_manager = db_manager.DatabaseManager()
    database_manager.add_bna_blocked_numbers(do_scraping=do_scraping)
    database_manager.add_bundesnetzagentur_given_numbers(parse_csv_file=parse_csv_file)
    database_manager.add_tellowsApi_actual_black_list(make_request=False)
    test_database()


def test_database():
    database_manager = db_manager.DatabaseManager.get_instance()
    db_session = database_manager.create_db_session()
    print(db_session.query(BlockedNumber).limit(20).all())
    print(db_session.query(GivenNumberBlock).limit(20).all())
    print(db_session.query(TellowsNumber).limit(20).all())
    db_session.close()


if __name__ == "__main__":
    start_server()


