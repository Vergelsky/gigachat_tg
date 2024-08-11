import requests
import json

import os
from dotenv import load_dotenv
load_dotenv('.env')

TOKEN = os.getenv('TG_TOKEN')
URL = 'https://api.telegram.org/bot'
MESSAGE = 'Хорошо сказано!'
offset = -2
text = ''


def get_updates(last_update=None) -> list:
    last_update = last_update if last_update else -2
    response = requests.get(f"{URL}{TOKEN}/getUpdates?offset={last_update + 1}")
    response = json.loads(response.text)
    return response['result'] if response['ok'] else None


def get_msg_properties(update):
    return update['message']['text'], update['message']['chat']['id'], update['update_id']


def send_message(answer, chat_id):
    resp = requests.get(f"{URL}{TOKEN}/sendMessage?text={answer}&chat_id={chat_id}")
    return resp.json()
