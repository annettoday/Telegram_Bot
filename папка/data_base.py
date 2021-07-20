import sqlite3
import datetime

def new_base():
    connect = sqlite3.connect('new_base2.db')
    cursor = connect.cursor()
    connect.commit()
    return cursor, connect


def table_user(message, name, email, phone):
    cursor, connect = new_base()
    user_id = message.chat.id
    cursor.execute("INSERT INTO users VALUES(?, ?, ?, ?)", (user_id, name, email, phone))
    connect.commit()

def check_in_field(user_id):
    cursor, connect = new_base()
    cursor.execute("""CREATE TABLE IF NOT EXISTS users( 
                   id integer PRIMARY KEY,
                   name_user text,
                   email_user text,
                   phone_user text
               )""")
    connect.commit()
    cursor.execute(f"SELECT id FROM users WHERE ID = {int(user_id)}")
    data = cursor.fetchone()
    return data

def table_data_user(message, org_inn, photo_1, photo_2, doc_pers_data):
    cursor, connect = new_base()
    cursor.execute("""PRAGMA foreign_keys=ON""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS data_user(
               chat_id INTEGER,
               date_time BLOB,
               org_inn TEXT,
               photo_passport_1 BLOB, 
               photo_passport_2 BLOB,
               doc_personal_data BLOB,
               FOREIGN KEY (chat_id) REFERENCES users(id)
           )""")
    user_id = message.chat.id
    cursor.execute("INSERT INTO data_user VALUES(?, ?, ?, ?, ?, ?)", (user_id, datetime.datetime.now, org_inn, photo_1, photo_2, doc_pers_data))
    connect.commit()