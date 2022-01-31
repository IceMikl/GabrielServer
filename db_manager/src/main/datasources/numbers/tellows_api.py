import ast
import json

import requests

from db_manager.src.main.config import config


class TellowsAPI:

    PATH_TO_JSON_FILE = config.PATH_TO_RESOURCES_FOLDER + 'tellows_actual_black_list.json'
    #PATH_TO_JSON_FILE = config.PATH_TO_RESOURCES_FOLDER + 'tellows_actual_black_list_test.json'

    def __init__(self):
        pass


    def get_actual_black_list(self, make_request=False):
        response = '[]'
        if(make_request):
            tellows_response = self.make_request_to_tellows()
            response = self.handle_response(tellows_response=tellows_response)
        else:
            with open(self.PATH_TO_JSON_FILE, 'r') as f:
                response = json.load(f)
                f.close()
        return response


    def handle_response(self, tellows_response):
        response_status = tellows_response.status_code
        response_json = '[]'
        if response_status == 200:
            response_body = tellows_response.content
            response_json = ast.literal_eval(response_body.decode('utf-8'))
            self.write_json_to_file(data_to_write=response_json)
        else:
            self.write_json_to_file(data_to_write=response_json)
        return response_json


    def make_request_to_tellows(self):
        REQUEST_URL = 'https://www.tellows.de/stats/partnerscoredata'
        params = {
            # 'partner': 'test',
            # 'apikey': 'test123',
            'apikeyMd5': '399a147c51f6942600fa41412f2678d1',
            'country': 'de',
            'lang': 'de',
            # 'userapikey': 'test123',
            'json': '1',
            'mosttagged': '1',
            'minscore': '1',
            'limit': '100000',
            'mincomments': '3',
            'showdeeplink': '1',
            'showcallertypeid': '1',
            'showcallername': '1',
            'showprefixname	': '1',
            'showlastcomment': '1',
            'numberformatinternational': '1',
            'anonymize': '0'
        }
        response = requests.get(REQUEST_URL, params=params)
        return response


    def write_json_to_file(self, data_to_write):
        with open(self.PATH_TO_JSON_FILE, 'wb') as f:
            f.write(json.dumps(data_to_write, indent=2).encode('utf-8'))
            f.close()


    def test_phone_number(self, phone_number='07812-1968053101'):
        REQUEST_URL = f'http://www.tellows.de/basic/num/{phone_number}?'
        headers = {
            'xml': '0',
            'partner': 'test',
            'apikey': 'test123'
        }
        response = requests.get(REQUEST_URL, headers=headers)
        response_status = response.status_code
        response_body = response.content
        print(f"REQUEST_URL: {REQUEST_URL} \n response_status: {response_status} \n response body: {response_body} \n")
        return response_body

