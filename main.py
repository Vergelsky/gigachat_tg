import json
import time

import db_commands
import sber_chat
import tg_bot

db_commands.create_table_users()


class User:
    def __init__(self, chat_id, last_update):
        self.chat_id = chat_id
        self.last_update = last_update
        db_commands.create_user_if_not_exist(self.chat_id, self.last_update)

    def add_history(self, added_history: list):
        old_history = self.get_history()
        old_history = json.loads(old_history) if old_history else []
        new_history = old_history + added_history if old_history else added_history
        db_commands.update_user(new_history, self.chat_id)

    def get_history(self):
        user = db_commands.get_user(self.chat_id)
        return user[0][1]

    def upgrade_update(self, update):
        db_commands.upgrade_update(self.chat_id, update)


def main():
    last_update = db_commands.get_last_update()
    updates = tg_bot.get_updates(last_update)
    for update in updates:
        message, chat_id, update_id = tg_bot.get_msg_properties(update)
        print(message)

        user = User(chat_id, update_id)

        history = user.get_history()
        history = json.loads(history) if history else []
        message_to_send = [{'role': 'user',
                            'content': message}]

        answer = sber_chat.send_question(history, message_to_send)
        print(answer)
        tg_bot.send_message(answer, chat_id)

        answer_to_add = [{'role': 'assistant',
                         'content': answer}]

        user.add_history(message_to_send + answer_to_add)
        user.upgrade_update(update_id)

while True:
    main()
    time.sleep(1)
