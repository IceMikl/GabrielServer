
import json
import scrapy
from scrapy.crawler import CrawlerProcess
from datetime import date
import re


class Bundesnetzagentur(scrapy.Spider):

    name = "bundesnetzagentur"
    custom_settings = {
        'DOWNLOAD_DELAY': 1
    }


    def start_requests(self):
        urls = [
            'https://www.bundesnetzagentur.de/DE/Vportal/TK/Aerger/Aktuelles/start.html#AnkerMassnahmen'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)


    def parse(self, response):
        new_data = []

        table_with_numbers = response.css('#content table')
        rows = table_with_numbers.xpath('./tbody/tr')

        for row in rows:
            number_object = {}
            for i, value in enumerate(row.xpath('./td')):
                if('xl' in value.xpath('./@class').get()):
                    if(i == 0):
                        number_object['date'] = value.xpath('./text()').get()
                    elif(i == 1):
                        text_value = value.xpath('./text()').get()
                        if self.is_a_list_of_numbers(text_value):
                            number_object['numbers_list'] = text_value.replace(' ', '').split(',')
                        else:
                            number_object['numbers_list'] = [text_value]
                    elif(i == 2):
                        number_object['category'] = value.xpath('./text()').get()
                    elif(i == 3):
                        number_object['action'] = value.xpath('./text()').get()
            if number_object != {}:
                new_data.append(number_object)

        self.write_new_data_to_file(new_data=new_data)


    def write_new_data_to_file(self, new_data):
        current_date = self.get_current_date_as_string()
        filename = f'resources/bundesnetzagentur_blocked_numbers_{current_date}.json'
        with open(filename, 'wb') as f:
            f.write(json.dumps(new_data, indent=2).encode('utf-8'))


    def get_current_date_as_string(self):
        today = date.today()
        return today.strftime("%d_%m_%y")

    def is_a_list_of_numbers(self, value):
        pattern = re.compile("([0-9]+((,)\s*)?)+")
        return pattern.match(value)


if __name__ == "__main__":
    process = CrawlerProcess()
    process.crawl(Bundesnetzagentur)
    process.start()



