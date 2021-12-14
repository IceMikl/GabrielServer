import requests

BASE = "http://127.0.0.1:5000/"

data = [{"likes": 78, "name": "Video 1", "views": 10000},
        {"likes": 1023, "name": "Video 2", "views": 79083},
        {"likes": 2341, "name": "Video_3", "views": 323}]

for i, videoData in enumerate(data):
    response = requests.put(BASE + "video/" + str(i), videoData)
    print(response.json())

response = requests.delete(BASE + "delete/0")
print(response)

input()

response = requests.get(BASE + "video/2")
print(response.json())