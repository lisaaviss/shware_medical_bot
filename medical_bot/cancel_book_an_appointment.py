import telebot
import os
from chat_messages import clear_patient_messages, add_message
from db_connection import create_db_connection

BOT_TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN, threaded=False)


def create_keyboard(buttons):
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(*buttons)
    return keyboard


def get_upcoming_visits_list(message):
    chat_id = str(message.chat.id)
    conn = create_db_connection()
    cur = conn.cursor()
    query = f'''SELECT d.name AS doctor_name, s.name AS specialization_name, a.appointment_time, a.appointment_date
                FROM "Appointments" AS a
                JOIN "Doctor" AS d ON a.doctor_id = d.id
                JOIN "Specialization" AS s ON a.specialization_id = s.id
                WHERE a.patient_id = (SELECT id FROM "Patient" WHERE chat_id = '{chat_id}') 
                and appointment_date >= CURRENT_DATE
                AND (
                    appointment_date != CURRENT_DATE
                    OR (appointment_date = CURRENT_DATE AND appointment_time > CURRENT_TIME)
                ) order by a.appointment_date ASC;'''
    cur.execute(query)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


def get_appointment_id(doc_name, spec, time, date):
    conn = create_db_connection()
    cur = conn.cursor()
    query = f'''SELECT a.id
                FROM "Appointments" AS a
                JOIN "Doctor" AS d ON a.doctor_id = d.id
                JOIN "Specialization" AS s ON a.specialization_id = s.id
                WHERE d.name = '{doc_name}'
                  AND s.name = '{spec}'
                  AND a.appointment_date = '{date}'
                  AND a.appointment_time = '{time}'; '''
    cur.execute(query)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


def cancel_book_appointment(delete_appointment_id):
    conn = create_db_connection()
    cur = conn.cursor()
    query = f'''UPDATE "Appointments" set patient_id = null where id = {delete_appointment_id}'''
    cur.execute(query)
    conn.commit()
    cur.close()
    conn.close()


def command_cancel_book_an_appointment(message):
    chat_messages = []
    chat_id = message.chat.id
    clear_patient_messages(chat_id)
    info_num = 0
    cancel_book_an_appointment_switcher(int(info_num), message, chat_messages)


def is_number(s):
    try:
        int(s)  # Пытаемся преобразовать строку в число
        return True
    except ValueError:
        return False


def cancel_book_an_appointment_switcher(cancel_book_an_appointment_num, message, chat_messages):
    def cancel_book_an_appointment_num0(message, chat_messages):
        chat_id = message.chat.id
        text = message.text
        column_name = 'command'
        print("Отправлено в добавление сообщения")
        add_message(text, column_name, chat_id)
        rows = get_upcoming_visits_list(message)
        if len(rows) == 0:
            bot.send_message(message.chat.id, "У вас нет записей на прием.")
        else:
            mess = 'Ваши записи на прием:\n'
            counter = 0
            visit_num = 0
            buttons = []
            for row in rows:
                visit_num += 1
                buttons.append(str(visit_num))
                doc_name = row[0]
                spec = row[1]
                time = row[2].strftime("%H:%M")
                date = row[3].strftime("%d.%m.%Y")
                mess += f"{visit_num}) {date} {time} \n{spec}: {doc_name}\n\n"
                counter += 1
                if counter % 10 == 0:
                    bot.send_message(message.chat.id, mess)
                    mess = ''
            if counter % 10 != 0:
                bot.send_message(message.chat.id, mess)
            keyboard = create_keyboard(buttons)
            bot.send_message(message.chat.id, "Выберите номер записи, которую хотите отменить.", reply_markup=keyboard)

    def cancel_book_an_appointment_num1(message, chat_messages):
        delete_row = message.text
        rows = get_upcoming_visits_list(message)
        print(rows)
        if is_number(delete_row):
            delete_row = int(delete_row)
            if 0 < delete_row <= len(rows):
                delete_row -= 1
                doc_name = rows[delete_row][0]
                spec = rows[delete_row][1]
                time = rows[delete_row][2]
                date = rows[delete_row][3]
                rows = get_appointment_id(doc_name, spec, time, date)
                print(rows)
                if len(rows) != 0:
                    delete_row_id = rows[0][0]
                    add_message(delete_row_id, 'msg1', message.chat.id)
                    mess = f"Вы подтверждаете отмену записи к врачу?"
                    buttons = ['ДА', 'НЕТ']
                    keyboard = create_keyboard(buttons)
                    print(mess)
                    bot.send_message(message.chat.id, mess, reply_markup=keyboard)
                else:
                    print("Произошло недоразумение в модуле cancel_book_an_appointment_num")

            else:
                bot.send_message(message.chat.id, "Введенный номер записи не существует."
                                                  "\nВыберите номер записи из списка.")
        else:
            bot.send_message(message.chat.id, "Введен некорректный номер записи."
                                              "\nВыберите номер записи из списка.")

    def cancel_book_an_appointment_num2(message, chat_messages):
        cancel_confirmation = message.text
        if cancel_confirmation.strip() == 'ДА':
            delete_appointment_id = chat_messages[1]
            cancel_book_appointment(delete_appointment_id)
            bot.send_message(message.chat.id, "Ваша запись отменена.")
            clear_patient_messages(message.chat.id)
        elif cancel_confirmation.strip() == 'НЕТ':
            bot.send_message(message.chat.id, "Ваша запись сохранена.")
            clear_patient_messages(message.chat.id)
        else:
            buttons = ['ДА', 'НЕТ']
            keyboard = create_keyboard(buttons)
            bot.send_message(message.chat.id, "Выберите \"ДА\" или \"НЕТ\"", reply_markup=keyboard)

    cases = {
        0: cancel_book_an_appointment_num0,
        1: cancel_book_an_appointment_num1,
        2: cancel_book_an_appointment_num2,
    }
    func = cases.get(cancel_book_an_appointment_num, lambda *args: print("Неизвестный случай1"))
    func(message, chat_messages)
