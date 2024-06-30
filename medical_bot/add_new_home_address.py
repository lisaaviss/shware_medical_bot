import telebot
import os
from datetime import datetime
from db_connection import create_db_connection
from chat_messages import clear_patient_messages, add_message

BOT_TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN, threaded=False)


def create_keyboard():
    buttons = ['Отсутствует']
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(*buttons)
    return keyboard


def command_add_new_home_address(message):
    chat_messages = []
    chat_id = message.chat.id
    print("Отправлено в очистку сообщений")
    clear_patient_messages(chat_id)
    info_num = 0
    add_new_home_address_switcher(int(info_num), message, chat_messages)


def add_new_home_address_switcher(add_new_home_address_num, message, chat_messages):
    def add_new_home_address_num0(message, chat_messages):
        chat_id = message.chat.id
        text = message.text
        column_name = 'command'
        print("Отправлено в добавление сообщения")
        add_message(text, column_name, chat_id)
        bot.send_message(message.chat.id, "Введите город", )

    def add_new_home_address_num1(message, chat_messages):
        chat_id = message.chat.id
        text = message.text
        column_name = 'msg1'
        print("Отправлено в добавление сообщения")
        add_message(text, column_name, chat_id)
        bot.send_message(message.chat.id, "Введите улицу")

    def add_new_home_address_num2(message, chat_messages):
        chat_id = message.chat.id
        text = message.text
        column_name = 'msg2'
        print("Отправлено в добавление сообщения")
        add_message(text, column_name, chat_id)
        keyboard = create_keyboard()
        bot.send_message(message.chat.id, "Введите номер дома\n\n"
                                          "Если номер дома отсутствует, нажмите кнопку \"Отсутствует\"", reply_markup=keyboard)

    def add_new_home_address_num3(message, chat_messages):
        chat_id = message.chat.id
        text = message.text
        if text == 'Отсутствует':
            text = ''
        column_name = 'msg3'
        print("Отправлено в добавление сообщения")
        add_message(text, column_name, chat_id)
        keyboard = create_keyboard()
        bot.send_message(message.chat.id, "Введите номер корпуса\n\n"
                                          "Если номер корпуса отсутствует, нажмите кнопку \"Отсутствует\"", reply_markup=keyboard)

    def add_new_home_address_num4(message, chat_messages):
        chat_id = message.chat.id
        text = message.text
        if text == 'Отсутствует':
            text = ''
        column_name = 'msg4'
        print("Отправлено в добавление сообщения")
        add_message(text, column_name, chat_id)
        keyboard = create_keyboard()
        bot.send_message(message.chat.id, "Введите литеру дома\n\n"
                                          "Если литера дома отсутствует, нажмите кнопку \"Отсутствует\"", reply_markup=keyboard)

    def add_new_home_address_num5(message, chat_messages):
        chat_id = message.chat.id
        text = message.text
        if text == 'Отсутствует':
            text = ''
        column_name = 'msg5'
        print("Отправлено в добавление сообщения")
        add_message(text, column_name, chat_id)
        keyboard = create_keyboard()
        bot.send_message(message.chat.id, "Введите номер подъезда\n\n"
                                          "Если подъезд отсутствует, нажмите кнопку \"Отсутствует\"", reply_markup=keyboard)

    def add_new_home_address_num6(message, chat_messages):
        chat_id = message.chat.id
        text = message.text
        if text == 'Отсутствует':
            text = ''
        column_name = 'msg6'
        print("Отправлено в добавление сообщения")
        add_message(text, column_name, chat_id)
        keyboard = create_keyboard()
        bot.send_message(message.chat.id, "Введите номер этажа\n\n"
                                          "Если номер этажа отсутствует, нажмите кнопку \"Отсутствует\"", reply_markup=keyboard)


    def add_new_home_address_num7(message, chat_messages):
        chat_id = message.chat.id
        text = message.text
        if text == 'Отсутствует':
            text = ''
        column_name = 'msg7'
        print("Отправлено в добавление сообщения")
        add_message(text, column_name, chat_id)
        keyboard = create_keyboard()
        bot.send_message(message.chat.id, "Введите номер квартиры\n\n"
                                          "Если номер квартиры отсутствует, нажмите кнопку \"Отсутствует\"", reply_markup=keyboard)

    def add_new_home_address_num8(message, chat_messages):
        chat_id = message.chat.id
        apartment_number = message.text
        apartment_number = message.text
        if apartment_number == 'Отсутствует':
            apartment_number = ''
        city_name = chat_messages[1]
        street_name = chat_messages[2]
        house_number = chat_messages[3]
        building_number = chat_messages[4]
        building_letter = chat_messages[5]
        entrance = chat_messages[6]
        floor = chat_messages[7]
        conn = create_db_connection()
        cur = conn.cursor()
        query = f'''insert into "Home_address" (patient_id, 
                    city_name, 
                    street_name, 
                    house_number, 
                    building_number, 
                    building_letter, 
                    entrance, 
                    floor, 
                    apartment_number) VALUES ((select id from "Patient" where chat_id='{chat_id}'),
                    '{city_name}', '{street_name}', '{house_number}', 
                    '{building_number}', '{building_letter}', '{entrance}', '{floor}', '{apartment_number}')'''
        cur.execute(query)
        if cur.rowcount > 0:
            print("INSERT успешно выполнен.")
        else:
            print("Ошибка при выполнении INSERT.")
        conn.commit()
        bot.send_message(message.chat.id, "Новый адрес успешно добавлен")
        cur.close()
        conn.close()

    cases = {
        0: add_new_home_address_num0,
        1: add_new_home_address_num1,
        2: add_new_home_address_num2,
        3: add_new_home_address_num3,
        4: add_new_home_address_num4,
        5: add_new_home_address_num5,
        6: add_new_home_address_num6,
        7: add_new_home_address_num7,
        8: add_new_home_address_num8
    }
    func = cases.get(add_new_home_address_num, lambda *args: print("Неизвестный случай1"))
    func(message, chat_messages)
