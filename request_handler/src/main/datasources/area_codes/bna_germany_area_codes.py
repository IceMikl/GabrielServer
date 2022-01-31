import csv
import json

from request_handler.src.main.config import config


class BNAGermanyAreaCodes:

    PATH_TO_CSV_FILE = config.PATH_TO_RESOURCES_FOLDER + 'bundesnetzagentur_germany_area_codes.csv'
    PATH_TO_JSON_FILE = config.PATH_TO_RESOURCES_FOLDER + 'bundesnetzagentur_germany_area_codes.json'

    def __init__(self):
        pass


    def get_area_codes(self, parse_csv_file):
        if(parse_csv_file):
            self.parse_csv_file()
        return self.read_json_file()


    def parse_csv_file(self):
        json_data = []
        with open(self.PATH_TO_CSV_FILE) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=';')
            line_count = 0
            headers = []
            for row in csv_reader:
                if line_count == 0:
                    line_count += 1
                    headers = row
                elif len(row) == len(headers):
                    json_object = {}
                    json_object['area_code'] = row[0]
                    json_object['place_name'] = row[1]
                    json_object['activ'] = row[2]
                    json_object['country'] = 'Germany'
                    line_count += 1
                    json_data.append(json_object)
            print(f'Processed {line_count} lines.')
        self.write_to_json_file(json_data)
        return json_data


    def write_to_json_file(self, json_data):
        with open(self.PATH_TO_JSON_FILE, 'wb') as f:
            f.write(json.dumps(json_data, indent=2).encode('utf-8'))
            f.close()


    def read_json_file(self):
        data = {}
        with open(self.PATH_TO_JSON_FILE, 'r') as f:
            data = json.load(f)
            f.close()
        return data