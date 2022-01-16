import ast
import csv
import json
import os
import logging

import requests
from xml.dom.minidom import parse as xml_parse
from xml.dom.minidom import parseString as xml_parseString

import xmltodict, json

from src.main.config import config

class SueddeutscheNewsApi:

    '''
    https://www.sueddeutsche.de/service/updates-mit-rss-uebersicht-aller-rss-feeds-fuer-sz-de-sz-magazin-und-jetzt-de-1.393950

    Geschäftliches Nutzen unserer RSS-Feeds ist nur nach Rücksprache mit uns (Anfragen bitte an marketing@sz.de) möglich,
    sobald Ihr Geschäftsmodell über die klassische Anzeigenfinanzierung Ihrer Seite hinausgeht. Wenn Sie zum Beispiel mit
     Hilfe unserer Feeds ein Bezahlangebot im Internet starten wollen, brauchen Sie vorher unsere Erlaubnis.
     Wenn Sie unsere Feeds 1:1 in Ihrem Blog einbinden, müssen Sie dies nicht. Wenn Sie Interesse an der Lizenzierung
     einzelner Artikel haben, wenden Sie sich bitte an zitat@sueddeutsche.de.

    '''


    PATH_TO_XML_FILE = config.PATH_TO_RESOURCES_FOLDER + 'news_sueddeutsche_zeitung_api.xml'
    PATH_TO_JSON_FILE = config.PATH_TO_RESOURCES_FOLDER + 'news_sueddeutsche_zeitung_api.json'

    def __init__(self):
        pass


    def get_news(self, make_request):
        if(make_request):
            self.request_actual_news()
        return self.read_json_file()


    def read_json_file(self):
        data = {}
        with open(self.PATH_TO_JSON_FILE, 'r') as f:
            data = json.load(f)
            f.close()
        return data


    def request_actual_news(self):
        response_raw = self.make_request_to_sueddeutsche_api()
        response_xml = self.handle_response(response_raw=response_raw)
        self.write_to_xml_file(data_to_write=response_xml)
        response_json = self.parse_xml_response()
        self.write_to_json_file(data_to_write=response_json)


    def make_request_to_sueddeutsche_api(self):
        REQUEST_URL = 'https://www.sueddeutsche.de/news/rss?all%5B%5D=dep&all%5B%5D=typ&all%5B%5D=sys&all%5B%5D=time'
        params = {
            'search': 'telefonbetrug',
            'sort': 'date'
        }
        response = requests.get(REQUEST_URL, params=params)
        return response



    def handle_response(self, response_raw):
        response_status = response_raw.status_code
        response_xml_string = ''
        if response_status == 200:
            response_body = response_raw.content
            response_xml_string = response_body.decode('utf-8')
        return response_xml_string


    def parse_xml_response(self):
        response_dict = dict()
        with open(self.PATH_TO_XML_FILE, 'r') as file:
            response_xml = file.read()
            file.close()
            response_dict = json.dumps(xmltodict.parse(response_xml))
        self.write_to_json_file(data_to_write=response_dict)
        return response_dict


    def write_to_json_file(self, data_to_write):
        with open(self.PATH_TO_JSON_FILE, 'wb') as f:
            f.write(json.dumps(data_to_write, indent=2).encode('utf-8'))
            f.close()


    def write_to_xml_file(self, data_to_write):
        with open(self.PATH_TO_XML_FILE, 'wb') as f:
            f.write(data_to_write.encode('utf-8'))
            f.close()