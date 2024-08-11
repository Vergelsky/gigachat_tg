import json
import requests

import os
from dotenv import load_dotenv
load_dotenv('.env')

client_secret = os.getenv("SBER_TOKEN")
auth_data = os.getenv("SBER_AUTH")
SBER_URL = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"
SCOPE = 'scope=GIGACHAT_API_PERS'
SBER_HEADERS = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept': 'application/json',
    'RqUID': '9d57c739-8266-4658-927e-aade84e5b347',
    'Authorization': f'Basic {auth_data}',
}
url_gigachat = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"


def get_access_token(sber_url, sber_headers, scope):
    resp = requests.request("POST", sber_url, headers=sber_headers, data=scope, verify=False)
    resp_text = resp.text
    return json.loads(resp_text)['access_token']


def send_question(history, message):
    payload = json.dumps({"model": "GigaChat",
               "messages": history + message if history else message,
               "stream": False,
               "repetition_penalty": 1}, ensure_ascii=False)
    access_token = get_access_token(SBER_URL, SBER_HEADERS, SCOPE)
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.request("POST", url_gigachat, headers=headers, data=payload, verify=False)
    answer = json.loads(response.text)["choices"][0]["message"]["content"]

    return answer
