import ast
import json

import requests
import xmltodict

from request_handler.src.main.config import config


class FazNewsApi:

    PATH_TO_JSON_FILE = config.PATH_TO_RESOURCES_FOLDER + 'news_faz_zeitung_api.json'


    def __init__(self):
        pass


    def get_news(self, make_request=False):
        if(make_request):
            self.make_request()
        return self.read_json_file()


    def make_request(self):
        REQUEST_URL = 'https://www.faz.net/rss/aktuell/gesellschaft/kriminalitaet/'
        response = requests.get(REQUEST_URL)
        response_status = response.status_code
        print(response_status)
        response_json = '[]'
        if response_status == 200:
            response_body = response.content
            response_xml = response_body.decode('utf-8')
            response_json = self.parse_xml_response(response_xml=response_xml)
        self.write_to_json_file(data_to_write=response_json)
        return response_json


    def parse_xml_response(self, response_xml):
        response_json = json.dumps(xmltodict.parse(response_xml))
        parsed_response = self.handle_response(response_json=response_json)
        return parsed_response


    def handle_response(self, response_json):
        if type(response_json)==str:
            response_json = ast.literal_eval(response_json)
        items = []
        for item in response_json['rss']['channel']['item']:
            if any(keyword in item['description'] for keyword in ['Telefonbetrug', 'Scam']):
                items.append(item)
        response_json['rss']['channel']['item'] = items
        return response_json


    def write_to_json_file(self, data_to_write):
        with open(self.PATH_TO_JSON_FILE, 'wb') as f:
            f.write(json.dumps(data_to_write, indent=2).encode('utf-8'))
            f.close()


    def read_json_file(self):
        data = {}
        with open(self.PATH_TO_JSON_FILE, 'r') as f:
            data = json.load(f)
            f.close()
        return data