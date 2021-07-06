from telebot import *
import test_sync
import json

bot = telebot.TeleBot('1806208816:AAEZaHOsy95Z3Yf347rTRzcpBO3Tg8g1g0w');


@bot.message_handler(content_types=['text'])



def get_text_messages(message):


    text = message.text
    if text.isdigit() and len(message.text)==10 or len(message.text)==12:
        bot.send_message(message.from_user.id, "№ {} принят".format(message.text))
        info1 = test_sync.find_by_id(text)

        #info = json.load(info1)
        obj_info = JsonInDict(info1)
        obj_info.Write()


        with open('file.json', 'r') as file:
            info = json.loads(file)

        if len(info) > 4096:
            for x in range(0, len(info), 4096):
                bot.send_message(message.chat.id, info[x:x + 4096])
        else:
            bot.send_message(message.chat.id, info)




    elif message.text == "/help":
        bot.send_message(message.from_user.id, "Введите ИНН: ")
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")
    return info


class JsonInDict(object):

    def __init__(self, info):
        self.info = info

    def Write(self):
        with open('file.json', 'w+') as file:
            file.write(self.info)




bot.polling(none_stop=True, interval=0)