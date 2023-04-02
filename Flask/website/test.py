from components_API import PackageName
import requests
BASE = 'http://127.0.0.1:5000/'
response = requests.put(BASE + 'package/43',{'Name':'Jack','Version':'1.1.1'})

