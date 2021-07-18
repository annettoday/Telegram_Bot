# -*- coding: utf-8 -*-

from telebot import *
import requests
import os


bot = telebot.TeleBot('1806208816:AAEZaHOsy95Z3Yf347rTRzcpBO3Tg8g1g0w')

URL = "https://suggestions.dadata.ru/suggestions/api/4_1/rs/findById/party"
TOKEN = "d6c4e6cc7f93ad1ff6b8e8c76528d501135eb7ec"

dict = {}
class User_photo_file:
    def __init__(self, name):
        self.name = name
        self.photo = None
        self.file = None


def get_request_dadata(message, inn):
    headers_auth = {'Authorization': 'Token ' + TOKEN, 'Content-Type': 'application/json'}
    auth = requests.post(URL, headers=headers_auth)
    if auth.status_code == 200:
        params = {
            'query': inn,
            'branch_type': "MAIN",
            'status': "ACTIVE"
        }
        try:
            r = requests.get(URL, headers=headers_auth, params=params)
            res = r.json()
            return res
        except Exception as e:
            bot.send_message(message.chat.id, e)
    else:
        return False

def get_info_about_org(message):
    try:
        data = get_request_dadata(message, message.text)
        if data == False:
            bot.send_message(message.from_user.id, "Не удалось получить ответа от сервера.")
        else:
            list_info_org = []
            list_info_org.append(data["suggestions"][0]["value"])
            list_info_org.append(
                data["suggestions"][0]["data"]["management"]["post"] + ": " +
                data["suggestions"][0]["data"]["management"][
                    "name"])
            list_info_org.append(data["suggestions"][0]["data"]["address"]["unrestricted_value"])

            bot.send_message(message.from_user.id, list_info_org[0] +
                             "\n{}".format(list_info_org[1]) +
                             "\nАдрес: {}".format(list_info_org[2])
                             )
    except Exception as e:
        bot.send_message(message.chat.id, "По данному ИНН не нашлось данных.")
        #некорректный результат после 1234567890
        #добавить кнопки

def buttons_connect_with_org(message):
    markup_reply = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    item_yes = types.KeyboardButton('Да')
    item_no = types.KeyboardButton('Нет')
    item_payment = types.KeyboardButton('Сделать перерасчёт')
    markup_reply.add(item_yes,  item_no)
    markup_reply.add(item_payment)
    bot.send_message(message.chat.id, "Вас интересует данная организация?", reply_markup=markup_reply)

def buttons_change_param(message):
    markup_reply = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    item_1 = types.KeyboardButton('Сделать перерасчёт')
    item_2 = types.KeyboardButton('Оформить зявку на лизинг')
    markup_reply.add(item_1,  item_2)
    bot.send_message(message.chat.id, "Выберите дальнейшее действие:", reply_markup=markup_reply)

def process_name_step(message):
    try:
        chat_id = message.chat.id
        name = message.from_user.first_name
        upload = User_photo_file(name)
        dict[chat_id] = upload
        a = telebot.types.ReplyKeyboardRemove()
        message = bot.send_message(chat_id, 'Загрузите фото паспорта: ', reply_markup=a)
        bot.register_next_step_handler(message, process_media_step)
    except Exception as e:
        bot.reply_to(message, 'Error...')

def process_media_step(message):
    try:
        chat_id = message.chat.id
        photo = message.photo[-1].file_id
        upload = dict[chat_id]
        upload.photo = photo
        bot.reply_to(message, "Ваше фото принято!")
        message = bot.send_message(message.chat.id, "Прикрепите согласие на обработку персональных данных: ")
        bot.register_next_step_handler(message, get_doc_from_user)
    except Exception as e:
        bot.reply_to(message, 'Ошибка. Попробуйте отправить снова.')
        bot.register_next_step_handler(message, process_media_step)

def get_doc_from_user(message):
    try:
        chat_id = message.chat.id
        file = bot.get_file(message.document.file_id)
        upload = dict[chat_id]
        upload.file = file
        bot.reply_to(message, "Ваше согл на обр перс данных принято!")
        message = bot.send_message(message.from_user.id,
                         "Отлично! Необходимые документы для оформления собраны. Теперь ознакомьтесь с офертой:")
        bot.register_next_step_handler(message, send_user_offer)
    except Exception as e:
        bot.reply_to(message, 'Ошибка')
        bot.register_next_step_handler(message, get_doc_from_user)

dict_calc = {}
def cost(message):
    try:
        cost_num = int(message.text)
        dict_calc[message.chat.id] = []
        dict_calc[message.chat.id].append(cost_num)

        if cost_num >= 1000000 and cost_num <= 20000000:
            message = bot.send_message(message.from_user.id,
                                       "Введите аванс в процентах, символ - % использовать не нужно")
            bot.register_next_step_handler(message, prepaid_expense)

        else:
            bot.reply_to(message, 'Недопустимое значение. Попробуйте ввести снова.')
            bot.register_next_step_handler(message, cost)
    except Exception as e:
        bot.reply_to(message, 'Недопустимое значение. Введите стоимость:')
        bot.register_next_step_handler(message, cost)

def prepaid_expense(message):
    try:
        prepaid_expense_num = int(message.text)
        dict_calc[message.chat.id].append(prepaid_expense_num)
        if prepaid_expense_num >= 0 and prepaid_expense_num <= 100:
            message = bot.send_message(message.from_user.id,
                                       "Введите срок лизинга в месяцах. Значение не должно превышать 60 мес. ")
            bot.register_next_step_handler(message, period)
        else:
            bot.reply_to(message, 'Недопустимое значение. Попробуйте ввести снова.')
            bot.register_next_step_handler(message, prepaid_expense)
    except Exception as e:
        bot.reply_to(message, 'Недопустимое значение. Введите аванс в процентах, символ - % использовать не нужно')
        bot.register_next_step_handler(message, prepaid_expense)

def period(message):
    try:
        period_num = int(message.text)
        dict_calc[message.chat.id].append(period_num)
        if period_num >= 12 and period_num <= 60:
            calculation_leasing(message)
        else:
            bot.reply_to(message, 'Недопустимое значение. Попробуйте ввести снова.')
            bot.register_next_step_handler(message, prepaid_expense)
    except Exception as e:
        bot.reply_to(message, 'Недопустимое значение. Введите срок лизинга в месяцах. Значение не должно превышать 60 мес.')
        bot.register_next_step_handler(message, period)

def calculation_leasing(message):
    bot.send_message(message.from_user.id,
                         f"По параметрам которые вы указали:\nстоимость: {dict_calc[message.chat.id][0]} руб.\nаванс: {dict_calc[message.chat.id][1]}% от стоимости\nсрок: {dict_calc[message.chat.id][2]} мес.\n\nСумма договора лизинга составляет:\nЕжемесячный платёж:\nОбщая сумма затрат с учётом выгоды по налогам:\nВозмещение НДС: ")
    buttons_change_param(message)

# def send_user_offer(message):
#     doc = open('/files/offer.txt', 'rb')
#     bot.send_document(message.chat.id, doc)
#     bot.send_document(message.chat.id, "FILEID")



def check_inn(message):
    if message.text.isdigit() and len(message.text) == 10 or len(message.text) == 12:
        get_info_about_org(message)
        buttons_connect_with_org(message)
    else:
        bot.send_message(message.from_user.id, "ИНН не корректен. Попробуйте ввести снова.")
        bot.register_next_step_handler(message, check_inn)

@bot.message_handler(commands=['start'])
def welcome(message):
    text_start = "Добрый день, {}! Мы поможем составить для вас график лизинговых платежей...\nДля получения оферты вам нужно будет предоставить:\n\n\t-ИНН Юр. Лица или ИП\n\t-Сканы паспорта. Необходимо прикрепить 2 страницы паспорта.\n\t-Согласие на обработку персональных данных. Прикрепленный документ должен быть в формате PDF\n\nДалее вам нужно будет указать параметры лизинговой сделки:\n\n\t -стоимость\n\t -аванс\n\t -срок".format(message.from_user.first_name)
    bot.send_message(message.chat.id, text_start)
    markup_reply = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item_leasing_payment = types.KeyboardButton('Расчёт лизинговых платежей')
    item_call = types.KeyboardButton('Оформить зявку на лизинг')
    markup_reply.add(item_leasing_payment, item_call)
    bot.send_message(message.chat.id, "Нажмите на кнопку, чтобы начать", reply_markup=markup_reply)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "Оформить зявку на лизинг":

        a = telebot.types.ReplyKeyboardRemove()
        message = bot.send_message(message.from_user.id, "Введите ИНН организации: ", reply_markup=a)
        bot.register_next_step_handler(message, check_inn)

    elif message.text == "Да":
        process_name_step(message)

    elif message.text == "Нет":
        a = telebot.types.ReplyKeyboardRemove()
        message = bot.send_message(message.from_user.id, "Проверьте верно ли вы указали ИНН. Введите снова: ", reply_markup=a)
        bot.register_next_step_handler(message, check_inn(message))

    elif message.text == 'Расчёт лизинговых платежей':
        bot.send_message(message.from_user.id, "Для рассчёта лизингового платежа, вам необходимо укакзать несколько параметров:\n\n - стоимость (в руб.)\n - аванс (в %)\n - срок (может варьироваться от 12 мес. до 60 мес.)")
        a = telebot.types.ReplyKeyboardRemove()
        message = bot.send_message(message.from_user.id, "Введите стоимость в рублях", reply_markup=a)
        bot.register_next_step_handler(message, cost)

    elif message.text == 'Сделать перерасчёт':
        a = telebot.types.ReplyKeyboardRemove()
        message = bot.send_message(message.from_user.id, "Введите стоимость в рублях", reply_markup=a)
        bot.register_next_step_handler(message, cost)


    # Инлайн кнопки
    # markup_inline = types.InlineKeyboardMarkup()
    # item_yes = types.InlineKeyboardButton(text='Да', callback_data='yes', one_time_keyboard=True)
    # item_no = types.InlineKeyboardButton(text='Нет', callback_data='no',  one_time_keyboard=True)
    # markup_inline.add(item_yes, item_no)
    # bot.send_message(message.chat.id, "Вас интересует данная организация?", reply_markup=markup_inline)

bot.polling(none_stop=True, interval=0)