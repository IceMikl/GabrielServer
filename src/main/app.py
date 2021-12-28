import sys

if("/" not in sys.path):
    sys.path.append("/")
print(sys.path)

from flask import Flask

import src.main.database.database_manager as db_manager
from src.main.database.models import BlockedNumber


app = Flask(__name__)

@app.route('/api/number/<string:phone_number>', methods=['GET'])
def check_phone_number(phone_number):
    database_manager = db_manager.DatabaseManager.get_instance()
    db_session = database_manager.create_db_session()

    blocked_number = db_session.query(BlockedNumber).filter_by(phone_number=phone_number).first()
    db_session.close()
    return {
               'phone_number': blocked_number.phone_number,
               'description': blocked_number.description,
               'suspicious': blocked_number.suspicious
           }, 200



def start_server():
    create_database(do_scaping=False, parse_given_numbers_csv=False)
    app.run(debug=True, use_reloader=False, port=8080, host="0.0.0.0")


def create_database(do_scaping=False, parse_given_numbers_csv=False):
    database_manager = db_manager.DatabaseManager()
    database_manager.add_bna_blocked_numbers(do_scaping=do_scaping)
    database_manager.add_bundesnetzagentur_given_numbers(parse_given_numbers_csv=parse_given_numbers_csv)

    test_database()


def test_database():
    print('asdf')
    blocked_number = BlockedNumber(phone_number="123", description="Some description", suspicious=9)
    database_manager = db_manager.DatabaseManager.get_instance()
    db_session = database_manager.create_db_session()
    print(f'db_session: {db_session}')
    db_session.add(blocked_number)
    db_session.commit()

    print(db_session.query(BlockedNumber).all())
    db_session.close()


if __name__ == "__main__":
    start_server()


