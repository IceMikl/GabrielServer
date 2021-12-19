import csv
import os


class BNAGivenNumbers:

    PATH_TO_SCRIPT = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    PATH_TO_FILE = PATH_TO_SCRIPT + '/resources/bundesnetzagentur_number_blocks.csv'

    def __init__(self):
        pass


    def get_given_number_blocks(self):
        return self.parse_csv_file()


    def parse_csv_file(self):
        json_data = []
        with open(self.PATH_TO_FILE) as csv_file:
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
                    json_object['phone_block_from'] = row[2]
                    json_object['phone_block_from'] = row[3]
                    json_object['block_size'] = row[4]
                    if(row[4] != '1000'):
                        print(row[4])
                    json_object['phone_provider'] = row[6]
                    line_count += 1
                    json_data.append(json_object)
            print(f'Processed {line_count} lines.')
        return json_data