import requests

URL = "http://127.0.0.1:8000/api/data"
HEADERS = {"X-User-Id": "1"}

for i in range(50):
    response = requests.get(URL, headers=HEADERS)
    print(i + 1, response.status_code, response.text)
