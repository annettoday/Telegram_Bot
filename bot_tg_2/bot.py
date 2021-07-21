# -*- coding: utf-8 -*-

from telebot import *
import requests
#import data_base
import base64

bot = telebot.TeleBot('1806208816:AAEZaHOsy95Z3Yf347rTRzcpBO3Tg8g1g0w')

URL = "https://suggestions.dadata.ru/suggestions/api/4_1/rs/findById/party"
TOKEN = "d6c4e6cc7f93ad1ff6b8e8c76528d501135eb7ec"

dict = {}

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
            bot.send_message(message.from_user.id, "Не удалось получить ответ от сервера.")
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
            buttons_connect_with_org(message)
    except Exception as e:
        a = telebot.types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, "По данному ИНН не нашлось данных.", reply_markup=a)
        message = bot.send_message(message.chat.id, "Введите ИНН:")
        bot.register_next_step_handler(message, get_info_about_org)


def buttons_connect_with_org(message):
    markup_reply = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    item_yes = types.KeyboardButton('Да')
    item_no = types.KeyboardButton('Нет')
    markup_reply.add(item_yes,  item_no)
    bot.send_message(message.chat.id, "Вас интересует данная организация?", reply_markup=markup_reply)

def buttons_change_param(message):
    markup_reply = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    item_1 = types.KeyboardButton('Сделать перерасчёт')
    item_2 = types.KeyboardButton('Оформить зявку на лизинг')
    markup_reply.add(item_1,  item_2)
    bot.send_message(message.chat.id, "Выберите дальнейшее действие:", reply_markup=markup_reply)

def buttons_regisrtation(message):
    markup_reply = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    item_1 = types.KeyboardButton('Отправить заявку')
    item_2 = types.KeyboardButton('Отменить зявку')
    item_3 = types.KeyboardButton('Расчёт лизинговых платежей')
    markup_reply.add(item_1,  item_2)
    markup_reply.add(item_3)
    bot.send_message(message.chat.id, "Выберите дальнейшее действие:", reply_markup=markup_reply)


dict_inn_photo_doc={}
def get_photo_1_from_user(message):
    try:
        file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        src = f'files/' + file_info.file_path
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)

        with open(src, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())

        dict_inn_photo_doc['pic_1'] = []
        dict_inn_photo_doc['pic_1'].append(encoded_string)

        message = bot.send_message(message.chat.id, "Прикрепите ещё одно фото: ")
        bot.register_next_step_handler(message, get_photo_2_from_user)

    except Exception as e:
        bot.reply_to(message, f'Ошибка. Попробуйте отправить снова. {e}')
        bot.register_next_step_handler(message, get_photo_1_from_user)

def get_photo_2_from_user(message):
    try:
        file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)

        downloaded_file = bot.download_file(file_info.file_path)
        src = f'files/' + file_info.file_path
        print(" src: ", src)
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)

        with open(src, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())

        dict_inn_photo_doc['pic_2'] = []
        dict_inn_photo_doc['pic_2'].append(encoded_string)

        message = bot.send_message(message.chat.id, "Прикрепите согласие об обраотке персональных данных: ")
        bot.register_next_step_handler(message,  get_doc_from_user)

    except Exception as e:
        bot.reply_to(message, 'Ошибка. Попробуйте отправить снова.')
        bot.register_next_step_handler(message, get_photo_2_from_user)

def get_doc_from_user(message):
    try:
        file_info = bot.get_file(message.document.file_id)

        downloaded_file = bot.download_file(file_info.file_path)
        src = f'files/doc/' + message.document.file_name
        print(" src: ", src)
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)

        with open(src, "rb") as doc_file:
            encoded_string = base64.b64encode(doc_file.read())

        dict_inn_photo_doc['doc'] = []
        dict_inn_photo_doc['doc'].append(encoded_string)

        #data_base.table_data_user(message, dict_inn_photo_doc['inn'][0], dict_inn_photo_doc['pic_1'][0],dict_inn_photo_doc['pic_2'][0], dict_inn_photo_doc['doc'][0])

        message = bot.send_message(message.from_user.id,"Введите стоимость:")
        bot.register_next_step_handler(message, cost_for_registration)

    except Exception as e:
        bot.reply_to(message, 'Ошибка. Попробуйте отправить снова.')
        bot.register_next_step_handler(message, get_doc_from_user)

dict_calc = {}
def cost_for_calc(message):
    try:
        if message.text.isdigit() and int(message.text) >= 1000000 and int(message.text) <= 20000000:
            dict_calc['cost'] = []
            dict_calc['cost'].append(int(message.text))

            message = bot.send_message(message.from_user.id,"Введите аванс в процентах, символ - % использовать не нужно.")
            bot.register_next_step_handler(message, prepaid_expense_for_calc)

        elif message.text == "/start":
            welcome(message)

        else:
            bot.reply_to(message, 'Недопустимое значение. Попробуйте ввести снова.')
            bot.register_next_step_handler(message, cost_for_calc)

    except Exception as e:
        bot.reply_to(message, 'Недопустимое значение. Введите стоимость:')
        bot.register_next_step_handler(message, cost_for_calc)

def prepaid_expense_for_calc(message):
    try:
        if message.text.isdigit() and int(message.text) >= 0 and int(message.text) <= 100:
            dict_calc['prepaid_expense'] = []
            dict_calc['prepaid_expense'].append(int(message.text))

            message = bot.send_message(message.from_user.id, "Введите срок лизинга в месяцах. Значение не должно превышать 60 мес. ")
            bot.register_next_step_handler(message, period_for_calc)

        elif message.text == "/start":
            welcome(message)

        else:
            bot.reply_to(message, 'Недопустимое значение. Попробуйте ввести снова.')
            bot.register_next_step_handler(message, prepaid_expense_for_calc)

    except Exception as e:
        bot.reply_to(message, 'Недопустимое значение. Введите аванс в процентах, символ - % использовать не нужно')
        bot.register_next_step_handler(message, prepaid_expense_for_calc)

def period_for_calc(message):
    try:
        if message.text.isdigit() and int(message.text)>= 12 and int(message.text) <= 60:
            dict_calc['period'] = []
            dict_calc['period'].append(int(message.text))
            calculation_leasing(message)

        elif message.text == "/start":
            welcome(message)

        else:
            bot.reply_to(message, 'Недопустимое значение. Попробуйте ввести снова.')
            bot.register_next_step_handler(message, period_for_calc)

    except Exception as e:
        bot.reply_to(message, 'Недопустимое значение. Введите срок лизинга в месяцах. Значение не должно превышать 60 мес.')
        bot.register_next_step_handler(message, period_for_calc)

def calculation_leasing(message):
    bot.send_message(message.from_user.id,f"По параметрам которые вы указали:\n\nстоимость: {dict_calc['cost'][0]} руб.\nаванс: {dict_calc['prepaid_expense'][0]}% от стоимости\nсрок: {dict_calc['period'][0]} мес.\n\nСумма договора лизинга составляет:\nЕжемесячный платёж:\nОбщая сумма затрат с учётом выгоды по налогам:\nВозмещение НДС: ")
    buttons_change_param(message)


def check_inn(message):
    if message.text.isdigit() and len(message.text) == 10 or len(message.text) == 12:
        dict_inn_photo_doc['inn'] = []
        dict_inn_photo_doc['inn'].append(message.text)
        get_info_about_org(message)

    elif message.text=="/start":
        welcome(message)

    else:
        message = bot.send_message(message.from_user.id, "ИНН не корректен. Попробуйте ввести снова.")
        bot.register_next_step_handler(message, check_inn)

dict_par={}

def cost_for_registration(message):
    try:
        if message.text.isdigit() and int(message.text) >= 1000000 and int(message.text) <= 20000000:
            dict_par['cost'] = []
            dict_par['cost'].append(int(message.text))

            message = bot.send_message(message.from_user.id, "Введите аванс в процентах, символ - % использовать не нужно.")
            bot.register_next_step_handler(message, prepaid_expense_for_registration)

        elif message.text == "/start":
            welcome(message)

        else:
            bot.reply_to(message, 'Недопустимое значение. Попробуйте ввести снова.')
            bot.register_next_step_handler(message, cost_for_registration)

    except Exception as e:
        bot.reply_to(message, 'Недопустимое значение. Введите стоимость:')
        bot.register_next_step_handler(message, cost_for_registration)

def prepaid_expense_for_registration(message):
    try:
        if message.text.isdigit() and int(message.text) >= 0 and int(message.text) <= 100:
            dict_par['prepaid_expense'] = []
            dict_par['prepaid_expense'].append(int(message.text))

            message = bot.send_message(message.from_user.id, "Введите срок лизинга в месяцах. Значение не должно превышать 60 мес. ")
            bot.register_next_step_handler(message, period_for_registration)

        elif message.text == "/start":
            welcome(message)

        else:
            bot.reply_to(message, 'Недопустимое значение. Попробуйте ввести снова.')
            bot.register_next_step_handler(message, prepaid_expense_for_registration)
    except Exception as e:
        bot.reply_to(message, 'Недопустимое значение. Введите аванс в процентах, символ - % использовать не нужно')
        bot.register_next_step_handler(message, prepaid_expense_for_registration)

def period_for_registration(message):
    try:
        if message.text.isdigit() and int(message.text)>= 12 and int(message.text) <= 60:
            dict_calc['period'] = []
            dict_calc['period'].append(int(message.text))
            send_offer(message)

        elif message.text == "/start":
            welcome(message)

        else:
            bot.reply_to(message, 'Недопустимое значение. Попробуйте ввести снова.')
            bot.register_next_step_handler(message, period_for_registration)
    except Exception as e:
        bot.reply_to(message, 'Недопустимое значение. Введите срок лизинга в месяцах. Значение не должно превышать 60 мес.')
        bot.register_next_step_handler(message, period_for_registration)


def send_offer(message):
    bot.send_message(message.chat.id, "Оферта: ляляляля")
    buttons_regisrtation(message)

dict_user = {}
def name_user(message):
    name_user = message.text
    dict_user[message.chat.id]=[]
    dict_user[message.chat.id].append(name_user)
    bot.send_message(message.chat.id, f"Приятно познакомиться, {name_user}!")
    message = bot.send_message(message.from_user.id, "Введите электронную почту:")
    bot.register_next_step_handler(message, email_user)

def email_user(message):
    email_user = message.text
    dict_user[message.chat.id].append(email_user)
    message = bot.send_message(message.from_user.id, "Введите ваш номер телефона:")
    bot.register_next_step_handler(message, phone_user)


def phone_user(message):
    phone_user = message.text
    dict_user[message.chat.id].append(phone_user)
    #data_base.table_user(message, dict_user[message.chat.id][0], dict_user[message.chat.id][1], dict_user[message.chat.id][2])
    message = bot.send_message(message.from_user.id, "Введите ИНН организации: ")
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
        # if data_base.check_in_field(message.chat.id) is None:
        #     a = telebot.types.ReplyKeyboardRemove()
        #     message = bot.send_message(message.from_user.id, "Введите ФИО: ", reply_markup=a)
        #     bot.register_next_step_handler(message, name_user)
        # else:
            a = telebot.types.ReplyKeyboardRemove()
            message = bot.send_message(message.from_user.id, "Введите ИНН: ", reply_markup=a)
            bot.register_next_step_handler(message, check_inn)

    elif message.text == "Да":
        a = telebot.types.ReplyKeyboardRemove()
        message = bot.send_message(message.from_user.id, 'Загрузите фото паспорта: ', reply_markup=a)
        bot.register_next_step_handler(message, get_photo_1_from_user)

    elif message.text == "Нет":
        a = telebot.types.ReplyKeyboardRemove()
        message = bot.send_message(message.from_user.id, "Проверьте верно ли вы указали ИНН. Введите снова: ", reply_markup=a)
        bot.register_next_step_handler(message, check_inn)

    elif message.text == 'Расчёт лизинговых платежей':
        bot.send_message(message.from_user.id, "Для рассчёта лизингового платежа, вам необходимо укакзать несколько параметров:\n\n - стоимость (в руб.)\n - аванс (в %)\n - срок (может варьироваться от 12 мес. до 60 мес.)")
        a = telebot.types.ReplyKeyboardRemove()
        message = bot.send_message(message.from_user.id, "Введите стоимость в рублях", reply_markup=a)
        bot.register_next_step_handler(message, cost_for_calc)

    elif message.text == 'Сделать перерасчёт':
        a = telebot.types.ReplyKeyboardRemove()
        message = bot.send_message(message.from_user.id, "Введите стоимость в рублях", reply_markup=a)
        bot.register_next_step_handler(message, cost_for_calc)

    elif message.text == 'Отменить зявку':
        pass
        #data_base.delete_from_data_user()

    # Инлайн кнопки
    # markup_inline = types.InlineKeyboardMarkup()
    # item_yes = types.InlineKeyboardButton(text='Да', callback_data='yes', one_time_keyboard=True)
    # item_no = types.InlineKeyboardButton(text='Нет', callback_data='no',  one_time_keyboard=True)
    # markup_inline.add(item_yes, item_no)
    # bot.send_message(message.chat.id, "Вас интересует данная организация?", reply_markup=markup_inline)




bot.polling(none_stop=True, interval=0)



#Конвертация файла из бд
# @bot.message_handler(commands=['img'])
# def ext_photo(message):
#     conn = sqlite3.connect("new_base3.db")
#     cursor = conn.cursor()
#     cursor.execute("""CREATE TABLE IF NOT EXISTS data_user(
#                chat_id INTEGER,
#                org_inn TEXT,
#                photo_passport_1 BLOB,
#                photo_passport_2 BLOB,
#                doc_personal_data BLOB,
#                FOREIGN KEY (chat_id) REFERENCES users(id)
#            )""")
#     img = conn.execute(f'SELECT doc_personal_data FROM data_user WHERE  chat_id = {message.chat.id}').fetchone()
#     print("img: ", img, "\ntype(img): ", type(img))
#     if img is None:
#         conn.close()
#         return None
#     else:
#         conn.close()
#
#         # сохраним base64 в картинку и отправим пользователю
#         with open("files/imageToSave.jpg", "wb") as fh:
#             fh.write(base64.decodebytes(img[0]))
#             bot.send_photo(message.chat.id, open("files/imageToSave.jpg", "rb"))