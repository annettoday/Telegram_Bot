
'''
import requests
from requests.exceptions import HTTPError

try:

    response = requests.key('dbbb221c31c1b727bdb84413b2b3d3776b743ea7')
    response.raise_for_status()
    # access JSOn content
    jsonResponse = response.json()
    print("Entire JSON response")
    print(jsonResponse)

except HTTPError as http_err:
    print(f'HTTP error occurred: {http_err}')
except Exception as err:
    print(f'Other error occurred: {err}')
'''

import requests
API_KEY = 'dbbb221c31c1b727bdb84413b2b3d3776b743ea7'
params = dict(key=API_KEY, text='Hello', lang='en-es')
res = requests.get(url, params=params)
print(params)
