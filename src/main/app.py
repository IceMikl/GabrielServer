import sys

if("/" not in sys.path):
    sys.path.append("/")
print(sys.path)


from sqlalchemy import and_
from flask import Flask

from phone_number_handler import PhoneNumberHandler
import src.main.database.database_manager as db_manager
from src.main.database.models import BlockedNumber, GivenNumberBlock


app = Flask(__name__)

@app.route('/api/number/<string:phone_number>', methods=['GET'])
def check_phone_number(phone_number):
    database_manager = db_manager.DatabaseManager.get_instance()
    db_session = database_manager.create_db_session()

    phone_number_handler = PhoneNumberHandler()
    phone_number_information = phone_number_handler.analyze_number(phone_number=phone_number)

    if(phone_number_information['valid']):
        national_number = phone_number_information['national_number']
        blocked_number = db_session.query(BlockedNumber).filter_by(phone_number=phone_number).first()
        if(blocked_number != None):
            return {
                       'phone_number': blocked_number.phone_number,
                       'description': blocked_number.description,
                       'suspicious': blocked_number.suspicious
                   }, 200
        else:
            # TODO: Implement request handler
            area_code = phone_number_information['area_code']
            if(area_code != ''):
                number_block = int(str(national_number).replace(str(area_code), '', 1))
                given_number_block = db_session.query(GivenNumberBlock).filter(
                    and_(GivenNumberBlock.area_code == area_code,
                         GivenNumberBlock.phone_block_from <= number_block,
                         GivenNumberBlock.phone_block_to >= number_block)
                ).first()
                if(given_number_block != None):
                    return {
                               'phone_number': national_number,
                               'description': 'This number is in the list of given numbers',
                               'area_code': given_number_block.area_code,
                               'phone_block_from': given_number_block.phone_block_from,
                               'phone_block_to': given_number_block.phone_block_to,
                               'place_name': given_number_block.place_name,
                               'phone_provider': given_number_block.phone_provider
                           }, 400
                else:
                    return {
                               'phone_number': national_number,
                               'description': 'Area code not found'
                           }, 400
            else:
                return {
                           'phone_number': national_number,
                           'description': 'Area code not found'
                       }, 400
    else:
        return {
                   'phone_number': phone_number,
                   'description': 'False phone number format'
               }, 400



def start_server():
    create_database(do_scaping=False, parse_csv_file=False)
    app.run(debug=True, use_reloader=False, port=8080, host="0.0.0.0")


def create_database(do_scaping=False, parse_csv_file=True):
    database_manager = db_manager.DatabaseManager()
    database_manager.add_bna_blocked_numbers(do_scaping=do_scaping)
    database_manager.add_bundesnetzagentur_given_numbers(parse_csv_file=parse_csv_file)

    test_database()


def test_database():
    database_manager = db_manager.DatabaseManager.get_instance()
    db_session = database_manager.create_db_session()
    print(db_session.query(BlockedNumber).limit(20).all())
    print(db_session.query(GivenNumberBlock).limit(20).all())
    db_session.close()


if __name__ == "__main__":
    start_server()


