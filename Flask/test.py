from website.components_API import *
import requests

BASE = 'http://localhost:8000/'
# BASE = 'https://module-registry-website-4a33ebcq3a-uc.a.run.app/'
test = ['https://github.com/lodash/lodash',
'https://github.com/chalk/chalk',
'https://github.com/moment/moment',
'https://github.com/webpack-contrib/css-loader',
'https://github.com/kriskowal/q']
headers = {'Content-Type': 'application/json'}
for URL in test:
    print(URL)
    response = requests.post(BASE + 'package',json={'URL': URL, 'ZipFile': None}, headers=headers)
    print('done')
    # print(response.content)

# uploadRatings(rate_Package('testfile.txt'))
# response = requests.delete(BASE + 'reset', headers=headers)
# print(response.content)