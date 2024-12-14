import json
import time
import hashlib
import hmac
import base64
import uuid
import requests
from dotenv import load_dotenv
import os

load_dotenv()

# Access the environment variables
token = os.getenv('SWITCHBOT_API_TOKEN')
secret = os.getenv('SWITCHBOT_API_SECRET')
# Declare empty header dictionary
apiHeader = {}
# open token
# secret key
nonce = uuid.uuid4()
t = int(round(time.time() * 1000))
string_to_sign = '{}{}{}'.format(token, t, nonce)

string_to_sign = bytes(string_to_sign, 'utf-8')
secret = bytes(secret, 'utf-8')

sign = base64.b64encode(hmac.new(secret, msg=string_to_sign, digestmod=hashlib.sha256).digest())
#Build api header JSON
apiHeader['Authorization']=token
apiHeader['Content-Type']='application/json'
apiHeader['charset']='utf8'
apiHeader['t']=str(t)
apiHeader['sign']=str(sign, 'utf-8')
apiHeader['nonce']=str(nonce)


def get_devices():
    url = 'https://api.switch-bot.com/v1.1/devices'
    response = requests.get(url, headers=apiHeader)
    if response.status_code == 200:
        json = response.json()
        print(json)
    else:
        print(f'Error: {response.status_code} - {response.text}')
        return None


if __name__ == "__main__":
    get_devices()

