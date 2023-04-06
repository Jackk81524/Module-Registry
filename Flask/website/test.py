from components_API import PackageName
import requests
BASE = 'http://127.0.0.1:5000/'
response = requests.post(BASE + 'packages',json = {'packages' : [{'Name':'Jack',},{'Name':'Jack2'}]})
print(response.text)
