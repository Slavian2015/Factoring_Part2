# KP638680

import requests

url = 'http://127.0.0.1:5000/api/v2/'

params = dict(
    report_type='full',
    search_phrase='KP638680'
)

resp = requests.get(url=url, params=params)
data = resp.json()

print(data)