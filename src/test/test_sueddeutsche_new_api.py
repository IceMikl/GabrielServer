import ast
import json

import xmltodict

from src.main.datasources.news.sueddeutsche_news_api import SueddeutscheNewsApi


sueddeutsche_news_api = SueddeutscheNewsApi()

def test_make_request_to_sueddeutsche_api():
    print('--- Test SueddeutscheNewsApi.test_make_request_to_sueddeutsche_api() ---')
    response = sueddeutsche_news_api.make_request_to_sueddeutsche_api()
    print(f"response: {response}")
    print(f"response status code: {response.status_code}")
    print(f"response content: {response.content.decode('utf-8')}")
    print(json.dumps(xmltodict.parse(response.content.decode('utf-8'))))
    print('--- ---')


def test_request_actual_news():
    sueddeutsche_news_api.request_actual_news()


def test_get_news_true():
    print(sueddeutsche_news_api.get_news(make_request=True))


def test_get_news_false():
    print(sueddeutsche_news_api.get_news(make_request=False))



if __name__ == '__main__':
    #test_make_request_to_sueddeutsche_api()
    #test_request_actual_news()
    test_get_news_true()
    test_get_news_false()