import json
import sqlite3


def create_table_users():
    # Устанавливаем соединение с базой данных
    with sqlite3.connect('my_database.db') as connection:
        cursor = connection.cursor()

        # Создаем таблицу Users
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users (
        chat_id INTEGER PRIMARY KEY,
        history TEXT,
        last_update INT
        )
        ''')

        # Сохраняем изменения и закрываем соединение
        connection.commit()


def get_user(chat_id: int) -> list:
    # Устанавливаем соединение с базой данных
    with sqlite3.connect('my_database.db') as connection:
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM Users WHERE chat_id = ?', (chat_id,))
        user = cursor.fetchall()
    return user


def create_user_if_not_exist(chat_id: int, last_update: int):
    user = get_user(chat_id)
    if not user:
        with sqlite3.connect('my_database.db') as connection:
            cursor = connection.cursor()
            cursor.execute('INSERT INTO Users (chat_id, last_update) VALUES (?, ?)',
                               (chat_id, last_update))
            # Сохраняем изменения и закрываем соединение
            connection.commit()


def update_user(history: list, chat_id: int):
    # Устанавливаем соединение с базой данных
    with sqlite3.connect('my_database.db') as connection:
        cursor = connection.cursor()


        # Обновляем возраст пользователя "newuser"
        cursor.execute('UPDATE Users SET history = ? WHERE chat_id = ?', (json.dumps(history, ensure_ascii=False), chat_id))

        # Сохраняем изменения и закрываем соединение
        connection.commit()


def get_last_update():
    # Устанавливаем соединение с базой данных
    with sqlite3.connect('my_database.db') as connection:
        cursor = connection.cursor()
        # Выбираем всех пользователей
        cursor.execute('SELECT MAX(last_update) FROM users')
        last_update = cursor.fetchall()[0][0]
    return last_update


def upgrade_update(chat_id, update):
    # Устанавливаем соединение с базой данных
    with sqlite3.connect('my_database.db') as connection:
        cursor = connection.cursor()

        # Обновляем возраст пользователя "newuser"
        cursor.execute('UPDATE Users SET last_update = ? WHERE chat_id = ?', (update, chat_id))

        # Сохраняем изменения и закрываем соединение
        connection.commit()
