import requests

BASE = "http://127.0.0.1:8080/"

data = [{"description": "First test phone number", "spam": True},
        {"description": "Second test phone number", "spam": False}]

for i, videoData in enumerate(data):
    response = requests.put(BASE + "api/number/" + str(i), videoData)
    response_status = response.status_code
    response_body = response.content
    print(f"response_status: {response_status}, response body: {response_body}")
    print(response.json())

'''
response = requests.delete(BASE + "delete/0")
print(response)

input()

response = requests.get(BASE + "video/2")
print(response.json())
'''