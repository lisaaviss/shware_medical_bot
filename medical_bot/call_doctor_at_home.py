import telebot
import os
from datetime import datetime
from chat_messages import clear_patient_messages, add_message
from db_connection import create_db_connection

BOT_TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN, threaded=False)


def create_keyboard(buttons):
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(*buttons)
    return keyboard

def check_calls(message):
    chat_id = int(message.chat.id)
    date = datetime.now().date()
    conn = create_db_connection()
    cur = conn.cursor()
    query = f'''select * from "Doctor_house_calls"
                where patient_id = (select id from "Patient" where chat_id = '{chat_id}') and call_date = '{date}' '''
    cur.execute(query)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


def command_call_doctor(message):
    chat_messages = []
    chat_id = message.chat.id
    print("Отправлено в очистку сообщений")
    clear_patient_messages(chat_id)
    info_num = 0
    call_doctor_switcher(int(info_num), message, chat_messages)


def get_home_address_list(message):
    chat_id = int(message.chat.id)
    conn = create_db_connection()
    cur = conn.cursor()
    query = f'''select city_name,
       street_name,
       house_number,
       building_number,
       building_letter,
       entrance,
       floor,
       apartment_number
       from "Home_address" where patient_id = (select id from "Patient" where chat_id = '{chat_id}')'''
    cur.execute(query)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


def get_home_address_id(message):
    chat_id = int(message.chat.id)
    conn = create_db_connection()
    cur = conn.cursor()
    query = f'''select id from "Home_address" where patient_id = (select id from "Patient" where chat_id = '{chat_id}')'''
    cur.execute(query)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


def add_call_doctor_record(message, address_id, date):
    chat_id = int(message.chat.id)
    conn = create_db_connection()
    cur = conn.cursor()
    query = f'''insert into "Doctor_house_calls" (patient_id, home_address_id, call_date) 
    values ((select id from "Patient" where chat_id = '{chat_id}'), {address_id}, '{date}')'''
    cur.execute(query)
    conn.commit()
    cur.close()
    conn.close()


def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


def call_doctor_switcher(call_doctor_num, message, chat_messages):
    def call_doctor_num_num0(message, chat_messages):
        chat_id = message.chat.id
        rows = check_calls(message)
        if len(rows) > 0:
            bot.send_message(message.chat.id, "Ваш вызов уже зарегистрирован.")
        else:
            text = message.text
            column_name = 'command'
            print("Отправлено в добавление сообщения")
            add_message(text, column_name, chat_id)
            rows = get_home_address_list(message)
            buttons = []
            if len(rows) > 0:
                mess = 'Выберите номер адреса или воспользуйтесь командой \"/add_new_home_address\" \nВаши адреса:\n'
                address_num = 0
                for row in rows:
                    city_name = row[0] if row[0] is not None else ""
                    street_name = row[1] if row[1] is not None else ""
                    house_number = row[2] if row[2] is not None else ""
                    building_number = row[3] if row[3] is not None else ""
                    building_letter = row[4] if row[4] is not None else ""
                    entrance = row[5] if row[5] is not None else ""
                    floor = row[6] if row[6] is not None else ""
                    apartment_number = row[7] if row[7] is not None else ""
                    address_num += 1
                    buttons.append(str(address_num))
                    mess += f"{address_num}) {city_name}, " \
                            f"{street_name}, " \
                            f"д. {house_number}, " \
                            f"к. {building_number}," \
                            f"лит. {building_letter}," \
                            f"подъезд {entrance}," \
                            f"этаж {floor}," \
                            f"кв. {apartment_number}\n\n"
                keyboard = create_keyboard(buttons)
                bot.send_message(message.chat.id, mess, reply_markup=keyboard)
            else:
                mess = "У вас нет ни одного адреса. Воспользуйтесь командой \"/add_new_home_address\", чтобы добавить адрес."
                bot.send_message(message.chat.id, mess)

    def call_doctor_num_num1(message, chat_messages):
        chosen_address = message.text
        if is_number(chosen_address):
            rows = get_home_address_list(message)
            chosen_address = int(chosen_address)
            if 0 < chosen_address <= len(rows):
                chosen_address -= 1
                rows = get_home_address_id(message)
                address_id = rows[chosen_address][0]
                date = datetime.now().date()
                add_call_doctor_record(message, address_id, date)
                bot.send_message(message.chat.id, "Ваш вызов зарегистрирован.")
                clear_patient_messages(message.chat.id)
            else:
                bot.send_message(message.chat.id, "По введенному номеру не найдено адреса. "
                                                  "Выберите номер адреса или воспользуйтесь командой \"/add_new_home_address\".")
        else:
            bot.send_message(message.chat.id, "По введенному номеру не найдено адреса. "
                                              "Выберите номер адреса или воспользуйтесь командой \"/add_new_home_address\".")

    cases = {
        0: call_doctor_num_num0,
        1: call_doctor_num_num1
    }
    func = cases.get(call_doctor_num, lambda *args: print("Неизвестный случай1"))
    func(message, chat_messages)
