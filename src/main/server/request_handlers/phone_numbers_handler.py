
from flask import Blueprint
from sqlalchemy import and_

from src.main.phone_number_handler import PhoneNumberHandler
import src.main.database.database_manager as db_manager
from src.main.database.models import BlockedNumber, GivenNumberBlock, TellowsNumber


phone_numbers = Blueprint('phone_numbers', __name__)


@phone_numbers.route('/check_number/<string:phone_number>', methods=['GET'])
def check_phone_number(phone_number):
    db_session = create_db_session()
    phone_number_information = parse_phone_number(phone_number=phone_number)

    answer = dict()
    if phone_number_information['valid']:
        national_number = phone_number_information['national_number']
        area_code = phone_number_information['area_code']

        blocked_number = db_session.query(BlockedNumber).filter_by(phone_number=phone_number).first()
        if blocked_number is not None:
            answer['block_number'] = answer_blocked_number_found(blocked_number=blocked_number)
        else:
            answer['block_number'] = answer_blocked_number_not_found(phone_number=phone_number, national_number=national_number)

        if area_code != '':
            number_block = int(str(national_number).replace(str(area_code), '', 1))
            given_number_block = db_session.query(GivenNumberBlock).filter(
                and_(GivenNumberBlock.area_code == area_code,
                     GivenNumberBlock.phone_block_from <= number_block,
                     GivenNumberBlock.phone_block_to >= number_block)
            ).first()
            if given_number_block is not None:
                answer['given_number_block'] = answer_given_number_block_found(
                    national_number=national_number,
                    given_number_block=given_number_block)
            else:
                answer['block_number'] = answer_given_number_block_not_found(
                    phone_number=phone_number, national_number=national_number)
        else:
            answer['area_code'] = answer_area_code_not_found(phone_number=phone_number, national_number=national_number)
    else:
        answer['phone_number'] = answer_phone_number_not_valid(phone_number=phone_number)

    return answer, 200



def create_db_session():
    database_manager = db_manager.DatabaseManager.get_instance()
    return database_manager.create_db_session()


def parse_phone_number(phone_number):
    phone_number_handler = PhoneNumberHandler()
    return phone_number_handler.analyze_number(phone_number=phone_number)


def answer_given_number_block_found(national_number, given_number_block):
    answer_dict = dict()
    answer_dict['phone_number'] = national_number,
    answer_dict['description'] = 'This number is in the list of given numbers',
    answer_dict['area_code'] = given_number_block.area_code,
    answer_dict['phone_block_from'] = given_number_block.phone_block_from,
    answer_dict['phone_block_to'] = given_number_block.phone_block_to,
    answer_dict['place_name'] = given_number_block.place_name,
    answer_dict['phone_provider'] = given_number_block.phone_provider
    return answer_dict


def answer_given_number_block_not_found(phone_number, national_number):
    answer_dict = dict()
    answer_dict['phone_number'] = phone_number
    answer_dict['national_number'] = national_number
    answer_dict['description'] = 'Given number not found'
    return answer_dict


def answer_blocked_number_found(blocked_number):
    answer_dict = dict()
    answer_dict['phone_number'] = blocked_number.phone_number,
    answer_dict['description'] = blocked_number.description,
    answer_dict['suspicious'] = blocked_number.suspicious
    return answer_dict


def answer_blocked_number_not_found(phone_number, national_number):
    answer_dict = dict()
    answer_dict['phone_number'] = phone_number
    answer_dict['national_number'] = national_number
    answer_dict['description'] = 'Area code not found'
    return answer_dict


def answer_area_code_not_found(phone_number, national_number):
    answer_dict = dict()
    answer_dict['phone_number'] = phone_number
    answer_dict['national_number'] = national_number
    answer_dict['description'] = 'Area code not found'
    return answer_dict


def answer_phone_number_not_valid(phone_number):
    answer_dict = dict()
    answer_dict['phone_number'] = phone_number
    answer_dict['description'] = 'False phone number format'
    return answer_dict

