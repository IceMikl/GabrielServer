
import logging as logger
import json
import os

import scrapy
from scrapy.crawler import CrawlerProcess
from datetime import date
import re


class Bundesnetzagentur(scrapy.Spider):

    FILENAME = 'datasources/resources/bundesnetzagentur_blocked_numbers.json'

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
        logger.info("Data from the request: " + str(response))
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
        logger.info("Data were scraped from Bundesnetzagentur")

        self.write_data_to_file(new_data=new_data)


    def write_data_to_file(self, new_data):
        print(os.listdir("."))
        with open(self.FILENAME, 'wb') as f:
            f.write(json.dumps(new_data, indent=2).encode('utf-8'))
            f.close()
        logger.info("Data were written into file")


    def get_data_from_file(self):
        print(os.listdir("."))
        #with open(self.FILENAME, 'r') as f:
        with open(self.FILENAME, 'r') as f:
            data = json.load(f)
            f.close()
        logger.info("Data were retrieved from file")
        return data


    def is_a_list_of_numbers(self, value):
        pattern = re.compile("([0-9]+((,)\s*)?)+")
        return pattern.match(value)


    def scrap_data(self):
        process = CrawlerProcess()
        process.crawl(Bundesnetzagentur)
        process.start()


    def get_actual_data(self):
        self.scrap_data()
        return self.get_data_from_file()



