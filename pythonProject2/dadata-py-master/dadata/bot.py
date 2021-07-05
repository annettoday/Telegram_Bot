from telebot import *
import test_sync
import json


bot = telebot.TeleBot('1806208816:AAEZaHOsy95Z3Yf347rTRzcpBO3Tg8g1g0w');

@bot.message_handler(content_types=['text'])

def get_text_messages(message):
    text = message.text
    if text.isdigit() and len(message.text)==10  or len(message.text)==12:
        bot.send_message(message.from_user.id, "№ {} принят".format(message.text))
        info = test_sync.find_by_id(str(text))
        #info = jsonInDict(info1)
        if len(info) > 4096:
            for x in range(0, len(info), 4096):
                bot.send_message(message.chat.id, info[x:x + 4096])
        else:
            bot.send_message(message.chat.id, info)
        bot.send_message(message.from_user.id, "Info: {}".format(info))
    elif message.text == "/help":
        bot.send_message(message.from_user.id, "Введите ИНН: ")
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")

#def jsonInDict(info):
#   infoInDict = json.load(info, ensure_ascii = False, indent=4, sort_keys=True)
#    return infoInDict


bot.polling(none_stop=True, interval=0)