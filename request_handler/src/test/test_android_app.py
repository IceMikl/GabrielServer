import base64
import requests
from requests.auth import HTTPBasicAuth


def personal_access_token():
    base_url = 'https://api.sipgate.com/v2'
    token_id = 'token-MZO9UZ'
    token = '64475f6b-10f9-4dff-a568-74f3f7a515ba'

    credentials = (token_id + ':' + token).encode('utf-8')
    base64_encoded_credentials = base64.b64encode(credentials).decode('utf-8')

    headers = {
        'Authorization': 'Basic ' + base64_encoded_credentials
    }

    response = requests.get(base_url + '/account', headers=headers)

    print('Status:', response.status_code)
    print('Body:', response.content.decode("utf-8"))



def outgoing_call():
    base_url = 'https://api.sipgate.com/v2'

    token_id = 'token-6U8W67'
    token = '93ac36b4-8fbd-4969-95f6-2c136b900596'

    device_id = '3270296e1'
    caller = '3270296e1'

    callee = '+491628497957'
    caller_id = '+491579-2356114'

    headers = {
        'Content-Type': 'application/json'
    }

    request_body = {
        "deviceId": device_id,
        "callee": callee,
        "caller": caller,
        "callerId": caller_id
    }

    response = requests.post(
        base_url + '/sessions/calls',
        json=request_body,
        auth=HTTPBasicAuth(token_id, token),
        headers=headers
    )

    print('Status:', response.status_code)
    print('Body:', response.content.decode("utf-8"))
    print('Reason:', response.reason)


if __name__ == "__main__":
    outgoing_call()


