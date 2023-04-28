from website.components_API import *
import requests

BASE = 'http://localhost:8000/'
# BASE = 'https://module-registry-website-4a33ebcq3a-uc.a.run.app/'
test = ['https://github.com/lodash/lodash',
'https://github.com/chalk/chalk',
'https://github.com/moment/moment',
'https://github.com/webpack-contrib/css-loader',
'https://github.com/kriskowal/q']

## TEST upload /package
'''
headers = {'Content-Type': 'application/json'}
for URL in test:
    print(URL)
    response = requests.post(BASE + 'package',json={'URL': URL, 'ZipFile': None,'JSProgram': 'None'}, headers=headers)
    print('done')
    # print(response.content)
'''
## TEST get list of packages /packages
headers = {'Content-Type': 'application/json'}
test = [{'Name' : 'lodash','Version' : '5.0.0'}, # Should work
        {'Name' : 'css-loader','Version' : '6.7.3'}, # Should work
        {'Name' : 'chalk'}, # Should work
        {'Name' : 'chalk2','Version' : '5.2.0'}, # Should not work
        {'Name' : 'q','Version' : '1.5.2'}] # Should not work 
response = requests.post(BASE + 'packages',json = test,headers = headers)
print(response.json())

