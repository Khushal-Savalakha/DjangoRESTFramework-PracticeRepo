import requests
import json

URL = "http://127.0.0.1:8000/stucreate/"

data = {
    'name': 'sonam',
    'roll': 101,
    'city': 'Ranchi'
}

headers = {
    'Content-Type': 'application/json'
}

response = requests.post(url=URL, data=json.dumps(data), headers=headers)

print("Response Status Code:", response.status_code)
print("Response Content:", response.text)
print("Response Headers:", response.headers)

# Only try to decode JSON if the response is valid
if response.headers.get('Content-Type') == 'application/json':
    data = response.json()
    print(data)
else:
    print("Response is not JSON format.")
