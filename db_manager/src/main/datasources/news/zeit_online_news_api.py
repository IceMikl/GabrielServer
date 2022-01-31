import ast

import requests


class ZeitOnlineApi:

    def __init__(self):
        pass


    def make_request(self, keyword):
        REQUEST_URL = f'https://api.zeit.de/keyword'
        params = {
            'q': 'Betrug',
            'limit': 3
        }
        headers = {
            'X-Authorization': 'd3c1be18dd09c7195e369336b6de2f3b7b6f843fbf2fa092190b'
        }
        response = requests.get(REQUEST_URL, params=params, headers=headers)
        response_status = response.status_code
        print(response_status)
        response_json = '[]'
        if response_status == 200:
            response_body = response.content
            response_json = ast.literal_eval(response_body.decode('utf-8'))
        return response_json
