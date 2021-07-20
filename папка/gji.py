# -*- coding: utf-8 -*-
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton,  InputMediaPhoto
import sqlite3
from pathlib import Path
import base64
import codecs

bot = telebot.TeleBot('1806208816:AAEZaHOsy95Z3Yf347rTRzcpBO3Tg8g1g0w')

# Сохраним изображение, которое отправил пользователь в папку `/files/%ID пользователя/photos`
@bot.message_handler(content_types=['photo'])
def save_photo(message):
    # создадим папку если её нет
    Path(f'files/photos').mkdir(parents=True, exist_ok=True)

    # сохраним изображение
    file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    src = f'files/{message.chat.id}/' + file_info.file_path
    with open(src, 'wb') as new_file:
        new_file.write(downloaded_file)




    # явно указано имя файла!
    # откроем файл на чтение  преобразуем в base64
    with open(f'files/{message.chat.id}/photos/file_0.jpg', "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())

    # откроем БД и запишем информацию (ID пользователя, base64, подпись к фото)
    conn = sqlite3.connect("test.db")
    cursor = conn.cursor()
    cursor.execute('INSERT INTO users VALUES (?, ?, ?)', (message.chat.id, encoded_string, str(message.caption)))
    conn.commit()


# при получении команды /img от пользователя
@bot.message_handler(commands=['img'])
def ext_photo(message):
    # откроем БД и по ID пользователя извлечём данные base64
    conn = sqlite3.connect("new_base2.db")
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS data_user(
               chat_id INTEGER,
               org_inn TEXT,
               photo_passport_1 BLOB, 
               photo_passport_2 BLOB,
               doc_personal_data BLOB,
               FOREIGN KEY (chat_id) REFERENCES users(id)
           )""")
    img = conn.execute(f'SELECT photo_passport_1 FROM data_user WHERE  chat_id = {message.chat.id}').fetchone()
    print("img: ", img, "\ntype(img): ", type(img))
    if img is None:
        conn.close()
        return None
    else:
        conn.close()

        # сохраним base64 в картинку и отправим пользователю
        with open("files/imageToSave.jpg", "wb") as fh:
            fh.write(base64.b64decode(", ".join(img)))
            bot.send_photo(message.chat.id, open("files/imageToSave.jpg", "rb"))

bot.polling()
