import requests

import scrapy
from scrapy.crawler import CrawlerProcess

from datetime import date

import re



class Bundesnetzagentur:

    def __init__(self):
        pass


    def getBlockedNumbers(self):
        response = requests.get("https://www.bundesnetzagentur.de/DE/Vportal/TK/Aerger/Aktuelles/start.html#AnkerMassnahmen")
        print(response.status_code)
        print(response.content)



class QuotesSpider(scrapy.Spider):

    name = "bundesnetzagentur"
    custom_settings = {
        'DOWNLOD_DELAY': 1
    }

    def start_requests(self):
        urls = [
            'https://www.bundesnetzagentur.de/DE/Vportal/TK/Aerger/Aktuelles/start.html#AnkerMassnahmen'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        current_date = self.get_current_date_as_string()
        filename = f'bundesnetzagentur_{current_date}.html'
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log(f'Saved file {filename}')

        table_with_numbers = response.css('#content table')
        rows = table_with_numbers.xpath('./tbody/tr')

        for row in rows:
            print('')
            for i, value in enumerate(row.xpath('./td')):
                if('xl' in value.xpath('./@class').get()):
                    if(i == 0):
                        date = value.xpath('./text()').get()
                        print(f'date: {date}')
                    elif(i == 1):
                        text_value = value.xpath('./text()').get()
                        if self.is_a_list_of_numbers(text_value):
                            numbers_list = text_value.replace(' ', '').split(',')
                        else:
                            numbers_list = [text_value]
                        print(f'numbers: {str(numbers_list)}')
                    elif(i == 2):
                        category = value.xpath('./text()').get()
                        print(f'category: {category}')
                    elif(i == 3):
                        action = value.xpath('./text()').get()
                        print(f'action: {action}')



    def get_current_date_as_string(self):
        today = date.today()
        return today.strftime("%d_%m_%y")

    def is_a_list_of_numbers(self, value):
        pattern = re.compile("([0-9]+((,)\s*)?)+")
        return pattern.match(value)

if __name__ == "__main__":
    #bundesnetzagentur = Bundesnetzagentur()
    #bundesnetzagentur.getBlockedNumbers()

    process = CrawlerProcess()
    process.crawl(QuotesSpider)
    process.start()

