import telebot
import os
from datetime import datetime
from db_connection import create_db_connection
from chat_messages import clear_patient_messages, add_message

BOT_TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN, threaded=False)


def create_keyboard(buttons):
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(*buttons)
    return keyboard


def command_add_taken_medications(message):
    chat_messages = []
    chat_id = message.chat.id
    print("Отправлено в очистку сообщений")
    clear_patient_messages(chat_id)
    info_num = 0
    add_taken_medications_switcher(int(info_num), message, chat_messages)


def add_new_taken_medications_record(message, medication_name, start_date, end_date):
    chat_id = message.chat.id
    conn = create_db_connection()
    cur = conn.cursor()
    query = f'''insert into "Taken_medications" (patient_id, name, start_date, end_date) 
    values ((select id from "Patient" where chat_id = '{chat_id}'), '{medication_name}', '{start_date}', {end_date})'''
    cur.execute(query)
    if cur.rowcount > 0:
        print("INSERT успешно выполнен.")
    else:
        print("Ошибка при выполнении INSERT.")
    conn.commit()
    cur.close()
    conn.close()


def check_date(date_str):
    try:
        date_obj = datetime.strptime(date_str, '%d.%m.%Y')
        return date_obj.strftime('%Y-%m-%d')
    except ValueError:
        return False


def add_taken_medications_switcher(add_allergy_num, message, chat_messages):
    def add_taken_medications0(message, chat_messages):
        chat_id = message.chat.id
        text = message.text
        column_name = 'command'
        print("Отправлено в добавление сообщения")
        add_message(text, column_name, chat_id)
        bot.send_message(message.chat.id, "Введите название медикамента")

    def add_taken_medications1(message, chat_messages):
        medication_name = message.text
        add_message(medication_name, 'msg1', message.chat.id)
        bot.send_message(message.chat.id, "Введите дату начала приема медикаментов в формате dd.mm.yyyy\n"
                                          "Пример: 12.11.2009")

    def add_taken_medications2(message, chat_messages):
        start_date = message.text
        start_date = check_date(start_date)
        if start_date:
            buttons = ['по настоящее время']
            keyboard = create_keyboard(buttons)
            add_message(start_date, 'msg2', message.chat.id)
            bot.send_message(message.chat.id, "Введите дату конца приема медикаментов в формате dd.mm.yyyy\n"
                                              "Пример: 12.11.2009\n"
                                              "Или если до сих принимаете, нажмите кнопку \"по настоящее время\"", reply_markup=keyboard)

        else:
            bot.send_message(message.chat.id, "Введена некорректная дата. "
                                              "Введите дату начала приема медикаментов в формате dd.mm.yyyy\n"
                                              "Пример: 12.11.2009")

    def add_taken_medications3(message, chat_messages):
        end_date = message.text
        checked_end_date = check_date(end_date)
        if end_date == 'по настоящее время':
            end_date = 'null'
        elif checked_end_date:
            end_date = f"'{checked_end_date}'"
        else:
            end_date = 1
        if end_date != 1:
            medication_name = chat_messages[1]
            start_date = chat_messages[2]
            add_new_taken_medications_record(message, medication_name, start_date, end_date)
            bot.send_message(message.chat.id, "Принимаемые медикаменты успешно добавлены")
            clear_patient_messages(message.chat.id)
        else:
            buttons = ['по настоящее время']
            keyboard = create_keyboard(buttons)
            bot.send_message(message.chat.id, "Введена некорректная дата. "
                                              "Введите дату конца приема медикаментов в формате dd.mm.yyyy\n"
                                              "Пример: 12.11.2009\n"
                                              "Или если до сих принимаете, нажмите кнопку \"по настоящее время\"", reply_markup=keyboard)

    cases = {
        0: add_taken_medications0,
        1: add_taken_medications1,
        2: add_taken_medications2,
        3: add_taken_medications3

    }
    func = cases.get(add_allergy_num, lambda *args: print("Неизвестный случай1"))
    func(message, chat_messages)
