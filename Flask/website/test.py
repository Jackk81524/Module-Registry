from components_API import PackageName
import requests
BASE = 'http://127.0.0.1:5000/'
response = requests.get(BASE + 'package/31')
print(response.text)
