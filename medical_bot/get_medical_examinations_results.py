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


def get_examination_results(message, offset):
    chat_id = str(message.chat.id)
    conn = create_db_connection()
    cur = conn.cursor()
    query = f'''select e.name as ex_name, d.name as doc_name, s.name as spec_name, e.result, e.examination_date from "Medical_examination" as e
    join "Doctor" as d on e.doctor_id = d.id
    join "Specialization" as s on d.specialization_id = s.id
    where e.patient_id = (select id from "Patient" where chat_id = '{chat_id}') 
    order by e.examination_date desc  offset {int(offset)} limit 5;'''
    cur.execute(query)
    results = cur.fetchall()
    cur.close()
    conn.close()
    return results


def send_message(message, offset):
    results = get_examination_results(message, offset)
    if len(results) != 0:
        buttons = ['ЕЩЕ']
        add_message(str(offset), 'msg1', message.chat.id)
        mess = 'Ваши медицинские записи:\n\n'

        for row in results:
            result_name = row[0]
            doc_name = row[1] if row[1] is not None else ""
            spec_name = row[2] if row[2] is not None else ""
            result = row[3]
            creation_date = row[4].strftime("%d.%m.%Y")
            mess += f"Дата: {creation_date}\n\n" \
                    f"Врач: {spec_name} {doc_name}\n" \
                    f"Анализ: {result_name}\n" \
                    f"Результат: {result}\n\n"
            mess += "\n"
        mess += 'Нажмите кнопку \"ЕЩЕ\", чтобы вывести больше записей'
        keyboard = create_keyboard(buttons)
        bot.send_message(message.chat.id, mess, reply_markup=keyboard)
    else:
        clear_patient_messages(message.chat.id)
        bot.send_message(message.chat.id, "У вас нет результатов анализов")


def command_get_medical_examinations_results(message):
    chat_messages = []
    chat_id = message.chat.id
    print("Отправлено в очистку сообщений")
    clear_patient_messages(chat_id)
    info_num = 0
    get_medical_examinations_results_switcher(int(info_num), message, chat_messages)


def get_medical_examinations_results_switcher(get_medical_examinations_results_num, message, chat_messages):
    def get_medical_examinations_results_num0(message, chat_messages):
        chat_id = message.chat.id
        text = message.text
        column_name = 'command'
        print("Отправлено в добавление сообщения")
        add_message(text, column_name, chat_id)
        send_message(message, 0)

    def get_medical_examinations_results_num2(message, chat_messages):
        if message.text == 'ЕЩЕ':
            offset = int(chat_messages[1]) + 5
            send_message(message, offset)
        else:
            bot.send_message(message.chat.id, "Ошибка! Нажмите кнопку \"ЕЩЕ\", чтобы вывести больше записей")

    cases = {
        0: get_medical_examinations_results_num0,
        2: get_medical_examinations_results_num2,
    }
    func = cases.get(get_medical_examinations_results_num, lambda *args: print("Неизвестный случай1"))
    func(message, chat_messages)
