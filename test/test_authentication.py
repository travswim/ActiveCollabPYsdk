import requests
import json

import os
from dotenv import load_dotenv

load_dotenv()

url = os.getenv('AC_URL')
my_email = os.getenv('AC_EMAIL')
my_password = os.getenv(('AC_PASSWORD'))




if (url == None or my_email == None or my_password == None):
    raise ValueError(f'Cannot be empty value:\nurl = {url}\nmy_email = {my_email}\nmy_password = {my_password}')

data = {"email": my_email, "password": my_password}
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

try:
    r = requests.post(url=str(url), json=data, headers=headers)
    # r = requests.post(url, json=json.dumps(data), headers=headers)
    r.raise_for_status()  
except requests.HTTPError as e:
    raise SystemExit(e)

except requests.exceptions.RequestException as e:
    raise SystemExit(e)

print(r.status_code, r.reason)
print(json.dumps(r.json(), indent=4, sort_keys=True))
print(r.headers)