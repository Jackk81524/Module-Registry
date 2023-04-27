from website.components_API import *
import requests

BASE = 'http://127.0.0.1:8000/'
# BASE = 'https://module-registry-website-4a33ebcq3a-uc.a.run.app/'
test = ['https://github.com/lodash/lodash',
'https://github.com/chalk/chalk',
'https://github.com/tj/commander.js',
'https://github.com/moment/moment']
headers = {'Content-Type': 'application/json'}
for URL in test:
    response = requests.post(BASE + 'package',json={'URL': URL, 'ZipFile': None}, headers=headers)
    # print(response.content)
    input("Pass")

# uploadRatings(rate_Package('testfile.txt'))
# response = requests.post(BASE + 'package',json={'URL': 'https://github.com/Marak/colors.js', 'ZipFile': None}, headers=headers)
# print(response.content)