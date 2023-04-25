from website.components_API import *
import requests
import os
from dotenv import load_dotenv
import json
load_dotenv()
BASE = 'http://127.0.0.1:8000/'
response = requests.get(BASE + 'package/rate')

