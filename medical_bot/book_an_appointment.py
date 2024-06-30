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


def get_specializations_list():
    conn = create_db_connection()
    cur = conn.cursor()
    cur.execute('select name from "Specialization"')
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


def get_free_appointment_dates(chosen_doctor, chat_id):
    conn = create_db_connection()
    cur = conn.cursor()
    query = f'''SELECT DISTINCT appointment_date
    FROM "Appointments" AS a
    WHERE specialization_id = (SELECT id FROM "Specialization" WHERE name = '{chosen_doctor}')
      AND patient_id IS NULL
      AND appointment_date >= CURRENT_DATE
      AND NOT EXISTS (
        SELECT 1
        FROM "Appointments" AS a2
        WHERE a2.specialization_id = a.specialization_id
          AND a2.appointment_date = a.appointment_date
          AND a2.patient_id = (SELECT id FROM "Patient" WHERE chat_id = '{chat_id}')
      )
    ORDER BY appointment_date ASC;

    '''
    cur.execute(query)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


def get_free_appointment_times(chosen_doctor, chosen_date_obj):
    conn = create_db_connection()
    cur = conn.cursor()
    query = f'''select DISTINCT appointment_time from "Appointments" 
                    where specialization_id = (select id from "Specialization" where name = '{chosen_doctor}')
                    and patient_id is null and appointment_date = '{chosen_date_obj}' 
                    and (appointment_date != CURRENT_DATE
                    OR (appointment_date = CURRENT_DATE AND appointment_time > CURRENT_TIME)) 
                    ORDER BY appointment_time ASC'''
    cur.execute(query)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


def command_book_an_appointment(message):
    chat_messages = []
    chat_id = message.chat.id
    print("Отправлено в очистку сообщений")
    clear_patient_messages(chat_id)
    info_num = 0
    book_appointment_switcher(int(info_num), message, chat_messages)


def book_appointment_switcher(book_appointment_num, message, chat_messages):
    def book_appointment_num0(message, chat_messages):
        chat_id = message.chat.id
        text = message.text
        column_name = 'command'
        print("Отправлено в добавление сообщения")
        add_message(text, column_name, chat_id)
        buttons = []
        rows = get_specializations_list()
        if len(rows) != 0:
            for row in rows:
                buttons.append(row[0])
        else:
            print("Возникла проблема, нет специализаций, модуль book_an_appointment0")
        keyboard = create_keyboard(buttons)
        bot.send_message(message.chat.id, "Выберите специализацию врача.", reply_markup=keyboard)

    def book_appointment_num1(message, chat_messages):
        chosen_doctor = message.text
        doctors = []
        rows = get_specializations_list()
        if len(rows) != 0:
            for row in rows:
                doctors.append(row[0])
        else:
            print("Возникла проблема, нет специализаций, модуль book_an_appointment1")
        if chosen_doctor in doctors:
            buttons = []
            rows = get_free_appointment_dates(chosen_doctor, str(message.chat.id))
            if len(rows) != 0:
                for row in rows:
                    buttons.append(row[0].strftime("%d.%m"))
                add_message(chosen_doctor, 'msg1', message.chat.id)
                keyboard = create_keyboard(buttons)
                bot.send_message(message.chat.id, "Выберите дату посещения.",
                             reply_markup=keyboard)
            else:
                bot.send_message(message.chat.id, "Для данного специалиста нет доступных дат для записи.\n"
                                                  "Выберите другого специалиста или попробуйте позже.")
        else:
            bot.send_message(message.chat.id, "Выбранный врач не существует, выберите врача из списка.")

    def book_appointment_num2(message, chat_messages):
        chosen_doctor = chat_messages[1]
        chosen_date = message.text
        dates = []
        rows = get_free_appointment_dates(chosen_doctor, str(message.chat.id))
        if len(rows) != 0:
            for row in rows:
                dates.append(row[0].strftime("%d.%m"))
        else:
            bot.send_message(message.chat.id, "Запись на выбранную дату невозможна, перезапустите команду и выберите другую дату")
        if chosen_date in dates:
            buttons = []
            chosen_date_obj = datetime.strptime(chosen_date + '.' + str(datetime.now().year), "%d.%m.%Y").date()
            add_message(chosen_date_obj, 'msg2', message.chat.id)
            rows = get_free_appointment_times(chosen_doctor, chosen_date_obj)
            if len(rows) != 0:
                for row in rows:
                    buttons.append(row[0].strftime("%H:%M"))
            else:
                print("Возникла проблема, нет специализаций, модуль book_an_appointment2")
            keyboard = create_keyboard(buttons)
            bot.send_message(message.chat.id, "Выберите время посещения.", reply_markup=keyboard)
        else:
            bot.send_message(message.chat.id, "Введена некорректная дата, выберите дату из списка.")

    def book_appointment_num3(message, chat_messages):
        chosen_doctor = chat_messages[1]
        print(chat_messages[2])
        chosen_date = datetime.strptime(chat_messages[2], '%Y-%m-%d').date()
        chosen_time = message.text
        rows = get_free_appointment_times(chosen_doctor, chosen_date)
        times = []
        if len(rows) != 0:
            for row in rows:
                times.append(row[0].strftime("%H:%M"))
        else:
            bot.send_message(message.chat.id, "Запись на выбранное время невозможна, перезапустите команду и выберите другое время.")
        if chosen_time in times:
            chosen_time_obj = datetime.strptime(chosen_time, '%H:%M').time()
            print(chosen_time_obj)
            add_message(chosen_time_obj, 'msg3', message.chat.id)
            buttons = ['ДА', 'НЕТ']
            keyboard = create_keyboard(buttons)
            bot.send_message(message.chat.id, "Вы подтверждаете запись к врачу?", reply_markup=keyboard)
        else:
            bot.send_message(message.chat.id, "Введено некорректное время, выберите время из списка.")

    def book_appointment_num4(message, chat_messages):
        chat_id_str = message.chat.id
        chosen_doctor = chat_messages[1]
        chosen_date = datetime.strptime(chat_messages[2], '%Y-%m-%d').date()
        chosen_time_obj = chat_messages[3]
        cancel_confirmation = message.text
        if cancel_confirmation.strip() == 'ДА':
            conn = create_db_connection()
            cur = conn.cursor()
            query = f'''update "Appointments" set patient_id = (select id from "Patient" where chat_id = '{chat_id_str}') 
                        where specialization_id = (select id from "Specialization" where name = '{chosen_doctor}') 
                        and appointment_date = '{chosen_date}' and appointment_time='{chosen_time_obj}' '''
            print(query)
            cur.execute(query)
            conn.commit()
            cur.close()
            conn.close()
            clear_patient_messages(message.chat.id)
            keyboard = telebot.types.ReplyKeyboardMarkup()
            bot.send_message(message.chat.id, "Ваша запись успешно оформлена.", reply_markup=keyboard)
        elif cancel_confirmation.strip() == 'НЕТ':
            bot.send_message(message.chat.id, "Ваша запись отменена.")
            clear_patient_messages(message.chat.id)
        else:
            buttons = ['ДА', 'НЕТ']
            keyboard = create_keyboard(buttons)
            bot.send_message(message.chat.id, "Вы подтверждаете запись к врачу?\n"
                                              "Выберите \"ДА\" или \"НЕТ\".", reply_markup=keyboard)

    cases = {
        0: book_appointment_num0,
        1: book_appointment_num1,
        2: book_appointment_num2,
        3: book_appointment_num3,
        4: book_appointment_num4
    }
    func = cases.get(book_appointment_num, lambda *args: print("Неизвестный случай1"))
    func(message, chat_messages)
