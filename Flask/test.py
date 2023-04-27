from website.components_API import *
import requests
import os
from dotenv import load_dotenv
import json
load_dotenv()
BASE = 'http://127.0.0.1:5000/'
BASE = 'https://module-registry-website-4a33ebcq3a-uc.a.run.app/'
response = requests.delete(BASE + 'reset')
print(response.json())
# uploadRatings(rate_Package('testfile.txt'))
