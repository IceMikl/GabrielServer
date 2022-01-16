
from flask import Blueprint

import src.main.database.database_manager as db_manager
from src.main.database.models import AreaCode


area_codes = Blueprint('area_codes', __name__)


@area_codes.route('/get/<string:area_code>', methods=['GET'])
def check_area_code(area_code):
    area_code_information = handle_area_code(area_code)
    return area_code_information, 200


def create_db_session():
    database_manager = db_manager.DatabaseManager.get_instance()
    return database_manager.create_db_session()


def handle_area_code(area_code_str):
    area_code_information = dict()
    area_code_information['area_code'] = area_code_str
    try:
        area_code_int = int(area_code_str)
        db_session = create_db_session()
        area_code_object = db_session.query(AreaCode).filter_by(code=area_code_int).first()
        if area_code_object is not None:
            response = dict()
            response['place_name'] = area_code_object.place_name
            response['activ'] = area_code_object.activ
            response['country'] = area_code_object.country
            area_code_information['valid'] = True
            area_code_information['description'] = response
        else:
            area_code_information['valid'] = False
            area_code_information['description'] = 'Area code not found'
    except ValueError:
        print('[ERROR]: handle_area_code() ValueError')
        area_code_information['valid'] = False
        area_code_information['description'] = 'False code format'
    except:
        print('[ERROR]: handle_area_code()')
        area_code_information['description'] = 'Error on the server'
    return area_code_information



@area_codes.route('/get/all', methods=['GET'])
def get_all_area_codes():
    db_session = create_db_session()
    response = dict()
    area_codes = []
    area_code_objects = db_session.query(AreaCode).all()
    for area_code in area_code_objects:
        dict_object = dict()
        dict_object['code'] = area_code.code
        dict_object['place_name'] = area_code.place_name
        dict_object['activ'] = area_code.activ
        dict_object['country'] = area_code.country
        area_codes.append(dict_object)
    response['codes'] = area_codes
    return response, 200