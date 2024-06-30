import telebot
import os
from db_connection import create_db_connection
from chat_messages import clear_patient_messages
from chat_messages import add_message

BOT_TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN, threaded=False)


def create_keyboard(buttons):
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(*buttons)
    return keyboard


def get_records(message, offset):
    chat_id = str(message.chat.id)
    conn = create_db_connection()
    cur = conn.cursor()
    query = f'''select r.id, r.creation_date, s.name as sec_name, d.name as d_name, r.symptoms, r.diagnosis, r.treatment_plans, r.notes, o.name, o.link from "Medical_record" as r
            left join "Medical_objects" as o on r.id = o.record_id
            join "Doctor" as d  on r.doctor_id = d.id
            join "Specialization" as s on d.specialization_id = s.id where r.patient_id = (select id from "Patient" where chat_id = '{chat_id}') 
            order by creation_date desc
            offset {int(offset)} limit 3;'''
    cur.execute(query)
    results = cur.fetchall()
    cur.close()
    conn.close()
    return results


def send_message(message, offset):
    results = get_records(message, offset)
    if len(results) != 0:
        buttons = ['ЕЩЕ']
        add_message(str(offset), 'msg1', message.chat.id)
        mess = 'Ваши медицинские записи:\n\n'
        object_names = []
        object_links = []
        row_num = 0
        record_id = 0
        for row in results:
            record_id = row[0]
            # Проверяем, что индекс row_num + 1 не превышает длину списка results
            if row_num + 1 < len(results):
                if record_id == results[row_num + 1][0]:
                    o_name = row[8] if row[8] is not None else ""
                    o_link = row[9] if row[9] is not None else ""
                    object_names.append(o_name)
                    object_links.append(o_link)
                    row_num += 1
                    continue
            # Если индекс row_num + 1 превышает длину списка results, выполняем этот блок кода
            creation_date = row[1].strftime("%d.%m.%Y")
            spec_name = row[2]
            doc_name = row[3]
            symptoms = row[4]
            diagnosis = row[5]
            treatment_plans = row[6]
            notes = row[7] if row[7] is not None else ""
            o_name = row[8] if row[8] is not None else ""
            o_link = row[9] if row[9] is not None else ""
            object_names.append(o_name)
            object_links.append(o_link)
            mess += f"Дата: {creation_date}\n\n" \
                    f"Врач: {spec_name} {doc_name}\n\n" \
                    f"Симптомы: {symptoms}\n\n" \
                    f"Диагноз: {diagnosis}\n\n" \
                    f"Лечение: {treatment_plans}\n\n" \
                    f"Примечания: {notes}\n\n"
            object_num = 0
            for object_name in object_names:
                if object_name != "":
                    object_name += ':\n'
                mess += f"{object_name}" \
                        f"{object_links[object_num]}\n"
                object_num += 1
            mess += "\n"
            object_names.clear()
            object_links.clear()
            row_num += 1
        mess += 'Нажмите кнопку \"ЕЩЕ\", чтобы вывести больше записей'
        keyboard = create_keyboard(buttons)
        bot.send_message(message.chat.id, mess, reply_markup=keyboard)
    else:
        clear_patient_messages(message.chat.id)
        bot.send_message(message.chat.id, "У вас нет медицинских записей")


def command_get_medical_records(message):
    chat_messages = []
    chat_id = message.chat.id
    print("Отправлено в очистку сообщений")
    clear_patient_messages(chat_id)
    info_num = 0
    get_medical_records_switcher(int(info_num), message, chat_messages)


def get_medical_records_switcher(get_medical_records_num, message, chat_messages):
    def get_medical_records_num0(message, chat_messages):
        chat_id = message.chat.id
        text = message.text
        column_name = 'command'
        print("Отправлено в добавление сообщения")
        add_message(text, column_name, chat_id)
        send_message(message, 0)

    def get_medical_records_num2(message, chat_messages):
        if message.text == 'ЕЩЕ':
            offset = int(chat_messages[1]) + 3
            send_message(message, offset)
        else:
            bot.send_message(message.chat.id, "Ошибка! Нажмите кнопку \"ЕЩЕ\", чтобы вывести больше записей")

    cases = {
        0: get_medical_records_num0,
        2: get_medical_records_num2,
    }
    func = cases.get(get_medical_records_num, lambda *args: print("Неизвестный случай1"))
    func(message, chat_messages)
