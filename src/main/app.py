import sys

if("/" not in sys.path):
    sys.path.append("/")
print(sys.path)

from flask import Flask

import src.main.database.database_manager as db_manager
from src.main.database.models import BlockedNumber, GivenNumber


app = Flask(__name__)

@app.route('/api/number/<string:phone_number>', methods=['GET'])
def check_phone_number(phone_number):
    database_manager = db_manager.DatabaseManager.get_instance()
    db_session = database_manager.create_db_session()

    blocked_number = db_session.query(BlockedNumber).filter_by(phone_number=phone_number).first()
    if(blocked_number != None):
        return {
                   'phone_number': blocked_number.phone_number,
                   'description': blocked_number.description,
                   'suspicious': blocked_number.suspicious
               }, 200
    else:
        given_number = db_session.query(GivenNumber).filter_by(phone_number=phone_number).first()
        if(given_number != None):
            return {
                       'phone_number': given_number.phone_number,
                       'description': 'the number is in the list of given numbers',
                       'suspicious': 1
                   }, 200
        else:
            return {
                       'phone_number': phone_number,
                       'description': 'the number is not in the list of given numbers',
                       'suspicious': 6
                   }, 200



def start_server():
    create_database(do_scaping=False, parse_csv_file=False)
    app.run(debug=True, use_reloader=False, port=8080, host="0.0.0.0")


def create_database(do_scaping=False, parse_csv_file=False):
    database_manager = db_manager.DatabaseManager()
    database_manager.add_bna_blocked_numbers(do_scaping=do_scaping)
    database_manager.add_bundesnetzagentur_given_numbers(parse_csv_file=parse_csv_file)

    test_database()


def test_database():
    database_manager = db_manager.DatabaseManager.get_instance()
    db_session = database_manager.create_db_session()
    print(db_session.query(BlockedNumber).limit(20).all())
    print(db_session.query(GivenNumber).limit(20).all())
    db_session.close()


if __name__ == "__main__":
    start_server()


