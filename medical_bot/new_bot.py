import psycopg2
import requests
import telebot
import json
import os
from book_an_appointment import book_appointment_switcher, command_book_an_appointment
from db_connection import set_access_token, create_db_connection
from chat_messages import get_chat_messages
from get_upcoming_visits import command_get_upcoming_visits
from cancel_book_an_appointment import command_cancel_book_an_appointment, cancel_book_an_appointment_switcher
from call_doctor_at_home import call_doctor_switcher, command_call_doctor
from add_allergy import command_add_allergy, add_allergy_switcher
from add_taken_medications import add_taken_medications_switcher, command_add_taken_medications
from vaccination_calendar import command_vaccination_calendar
from get_medical_records import command_get_medical_records, get_medical_records_switcher
from get_medical_examinations_results import command_get_medical_examinations_results, \
    get_medical_examinations_results_switcher
from add_new_home_address import add_new_home_address_switcher, command_add_new_home_address
from get_appointment_schedule import command_get_appointment_schedule, get_appointment_schedule_switcher
from get_alleries import command_get_allergies
from get_taken_medications import command_get_medications

BOT_TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN, threaded=False)


def create_keyboard(buttons):
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(*buttons)
    return keyboard


def check_account(message):
    chat_id = message.chat.id
    conn = create_db_connection()
    cur = conn.cursor()
    query = f'''select chat_id from "Patient" where chat_id= '{chat_id}' '''
    cur.execute(query)
    results = cur.fetchall()
    cur.close()
    conn.close()
    if len(results) != 0:
        return True
    else:
        bot.send_message(message.chat.id, 'Авторизация не пройдена, воспользуйтесь командой /login')


@bot.message_handler(commands=["login"])
def login(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True)
    share_contact_button = telebot.types.KeyboardButton("Поделиться контактом", request_contact=True)
    keyboard.add(share_contact_button)
    bot.send_message(message.chat.id, "Для аутентификации нажмите кнопку \"Поделиться контактом\"",
                     reply_markup=keyboard)


@bot.message_handler(content_types=["contact"])
def handle_contact(message):
    print(message)
    if message.contact.user_id == message.from_user.id:
        phone_number = message.contact.phone_number
        print(phone_number)
        conn = create_db_connection()
        cur = conn.cursor()
        cur.execute('select number, chat_id from "Patient" where number = %(phone_number)s',
                    {"phone_number": phone_number})
        rows = cur.fetchall()
        if len(rows) == 0:
            bot.send_message(message.chat.id, "Обратитесь в медицинский центр для регистрации учетной записи")
        else:
            if rows[0][1] is None:
                cur.execute('update "Patient" set chat_id = (%(chat_id)s) where number = %(phone_number)s',
                            {"chat_id": str(message.chat.id), "phone_number": str(phone_number)})
                conn.commit()
                bot.send_message(message.chat.id, "Ваш аккаунт успешно зарегистрирован")
            else:
                bot.send_message(message.chat.id, "Ваш аккаунт успешно аутентифицирован")
        cur.close()
        conn.close()
    else:
        keyboard = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True)
        share_contact_button = telebot.types.KeyboardButton("Поделиться контактом", request_contact=True)
        keyboard.add(share_contact_button)
        bot.send_message(message.chat.id, "Присланный Вами контакт не соответствует вашему аккаунту telegram\n"
                                          "Для аутентификации нажмите кнопку \"Поделиться контактом\"",
                         reply_markup=keyboard)


@bot.message_handler(commands=["start"])
def start(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True)
    share_contact_button = telebot.types.KeyboardButton("Поделиться контактом", request_contact=True)
    keyboard.add(share_contact_button)
    bot.send_message(message.chat.id, "Для аутентификации нажмите кнопку \"Поделиться контактом\"",
                     reply_markup=keyboard)


@bot.message_handler(commands=["help"])
def help_command(message):
    print("Принял в работу команду help")
    mess = 'Список доступных команд:\n' \
           '/get_appointment_schedule - просмотр расписания приемов\n' \
           '/book_an_appointment - записаться к врачу на прием\n' \
           '/get_upcoming_visits - просмотр предстоящие посещений\n' \
           '/cancel_book_an_appointment - отменить запись на прием\n' \
           '/call_doctor_at_home - вызов врача на дом\n' \
           '/add_new_home_address - добавить новый домашний адрес\n' \
           '/add_allergy - добавить аллергию\n' \
           '/get_allergies - просмотр списка аллергий\n' \
           '/add_taken_medications - добавить принимаемые медикаменты\n' \
           '/get_taken_medications - просмотр принимаемых медикаментов\n' \
           '/vaccination_calendar - календарь прививок\n' \
           '/get_medical_records - просмотр медицинских записей\n' \
           '/get_medical_examinations_results - просмотр результатов анализов\n' \
           '/help - посмотреть список доступных команд'
    bot.send_message(message.chat.id, mess)


@bot.message_handler(commands=["book_an_appointment"])
def book_an_appointment(message):
    print("Принял в работу book_an_appointment")
    if check_account(message):
        command_book_an_appointment(message)


@bot.message_handler(commands=["get_upcoming_visits"])
def book_an_appointment(message):
    print("Принял в работу get_upcoming_visits")
    if check_account(message):
        command_get_upcoming_visits(message)


@bot.message_handler(commands=["get_medical_records"])
def get_medical_records(message):
    print("Принял в работу get_medical_records")
    command_get_medical_records(message)


@bot.message_handler(commands=["get_upcoming_visits"])
def book_an_appointment(message):
    print("Принял в работу get_upcoming_visits")
    command_get_upcoming_visits(message)


@bot.message_handler(commands=["cancel_book_an_appointment"])
def book_an_appointment(message):
    print("Принял в работу cancel_book_an_appointment")
    command_cancel_book_an_appointment(message)


@bot.message_handler(commands=["call_doctor_at_home"])
def book_an_appointment(message):
    print("Принял в работу call_doctor_at_home")
    command_call_doctor(message)


@bot.message_handler(commands=["add_allergy"])
def add_allergy(message):
    print("Принял в работу add_allergy")
    command_add_allergy(message)


@bot.message_handler(commands=["get_allergies"])
def get_allergies(message):
    print("Принял в работу get_allergies")
    command_get_allergies(message)


@bot.message_handler(commands=["get_appointment_schedule"])
def get_appointment_schedule(message):
    print("Принял в работу get_appointment_schedule")
    command_get_appointment_schedule(message)


@bot.message_handler(commands=["get_medical_examinations_results"])
def get_medical_examinations_results(message):
    print("Принял в работу get_medical_examinations_results")
    command_get_medical_examinations_results(message)


@bot.message_handler(commands=["add_taken_medications"])
def add_taken_medications(message):
    print("Принял в работу add_taken_medications")
    command_add_taken_medications(message)


@bot.message_handler(commands=["get_taken_medications"])
def get_taken_medications(message):
    print("Принял в работу get_taken_medications")
    command_get_medications(message)


@bot.message_handler(commands=["vaccination_calendar"])
def vaccination_calendar(message):
    print("Принял в работу vaccination_calendar")
    command_vaccination_calendar(message)


@bot.message_handler(commands=["add_new_home_address"])
def add_new_home_address(message):
    print("Принял в работу vaccination_calendar")
    command_add_new_home_address(message)


def command_switcher(command, message_count, message, chat_messages):
    cases = {
        "/book_an_appointment": book_appointment_switcher,
        "/cancel_book_an_appointment": cancel_book_an_appointment_switcher,
        "/call_doctor_at_home": call_doctor_switcher,
        "/add_allergy": add_allergy_switcher,
        "/add_taken_medications": add_taken_medications_switcher,
        "/get_medical_records": get_medical_records_switcher,
        "/get_medical_examinations_results": get_medical_examinations_results_switcher,
        "/add_new_home_address": add_new_home_address_switcher,
        "/get_appointment_schedule": get_appointment_schedule_switcher
    }
    func = cases.get(command, lambda *args: print("Неизвестный случай"))
    func(message_count, message, chat_messages)


@bot.message_handler(func=lambda message: True)
def handle_text(message):
    chat_id = message.chat.id
    chat_messages = get_chat_messages(chat_id)
    if len(chat_messages) > 0:
        message_count = int(len(chat_messages))
        command = str(chat_messages[0])
        print(command)
        command_switcher(command, message_count, message, chat_messages)
    else:
        bot.reply_to(message, "Что-то ввели не так. Пожалуйста, воспользуйтесь доступными командами.")


def handler(event, context):
    set_access_token(context.token["access_token"])
    message = json.loads(event["body"])
    update = telebot.types.Update.de_json(message)
    if update.message is not None:
        bot.process_new_updates([update])

    return {
        "statusCode": 200,
        "body": "ok",
    }
