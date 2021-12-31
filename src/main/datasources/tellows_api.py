import requests


class TellowsAPI:


    def __init__(self):
        pass



    def get_actual_black_list(self):
        REQUEST_URL = 'https://www.tellows.de/stats/partnerscoredata'
        params = {
            #'partner': 'test',
            #'apikey': 'test123',
            'apikeyMd5': '399a147c51f6942600fa41412f2678d1',
            'country': 'de',
            'lang': 'de',
            #'userapikey': 'test123',
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
        response_status = response.status_code
        response_body = response.content
        print(f"REQUEST_URL: {REQUEST_URL} \n response_status: {response_status} \n response body: {response_body} \n")



    def test_phone_number(self, phone_number_to_test ='07812-1968053101'):
        REQUEST_URL = f'http://www.tellows.de/basic/num/{phone_number_to_test}?'
        headers = {
            'xml': '1',
            'partner': 'test',
            'apikey': 'test123'
        }
        response = requests.get(REQUEST_URL, headers=headers)
        response_status = response.status_code
        response_body = response.content
        print(f"REQUEST_URL: {REQUEST_URL} \n response_status: {response_status} \n response body: {response_body} \n")

