import telebot
import os
from collections import defaultdict
from db_connection import create_db_connection
from chat_messages import clear_patient_messages, add_message
from datetime import datetime, timedelta

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


def get_schedule(message):
    doc_spec = message.text
    conn = create_db_connection()
    cur = conn.cursor()
    query = f'''SELECT
        d.name AS doc_name,
        a.appointment_date,
        a.appointment_time
    FROM
        "Appointments" AS a
    JOIN
        "Doctor" AS d
    ON
        d.id = a.doctor_id
    join "Doctor_offices" o on a.doctor_offices_id = o.id
    WHERE
        a.specialization_id = (SELECT id FROM "Specialization" WHERE name = '{doc_spec}') and
        appointment_date >= current_date
    ORDER BY
        d.name,
        a.appointment_date,
        a.appointment_time;'''
    cur.execute(query)
    results = cur.fetchall()
    cur.close()
    conn.close()
    return results


def command_get_appointment_schedule(message):
    chat_messages = []
    chat_id = message.chat.id
    print("Отправлено в очистку сообщений")
    clear_patient_messages(chat_id)
    info_num = 0
    get_appointment_schedule_switcher(int(info_num), message, chat_messages)


def get_appointment_schedule_switcher(appointment_schedule_num, message, chat_messages):
    def appointment_schedule_num0(message, chat_messages):
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
            print("Возникла проблема, нет специализаций, модуль appointment_schedule_num0")
        keyboard = create_keyboard(buttons)
        bot.send_message(message.chat.id, "Для просмотра расписания, выберите интересующую специализацию врача.", reply_markup=keyboard)



    def appointment_schedule_num1(message, chat_messages):
        chosen_doctor = message.text
        doctors = []
        rows = get_specializations_list()
        if len(rows) != 0:
            for row in rows:
                doctors.append(row[0])
        else:
            print("Возникла проблема, нет специализаций, модуль appointment_schedule_num1")

        if chosen_doctor in doctors:
            results = get_schedule(message)
            schedule = defaultdict(lambda: defaultdict(list))
            for row in results:
                name = row[0]
                date = row[1].strftime("%d.%m.%Y")
                time = row[2].strftime("%H:%M")
                schedule[name][date].append(time)

            output = ''
            for doctor_name, dates in schedule.items():
                output += f"Расписание: \n{message.text}: {doctor_name}\n"
                for date, times in sorted(dates.items()):
                    start_time = datetime.strptime(times[0], "%H:%M")
                    end_time = datetime.strptime(times[-1], "%H:%M") + timedelta(minutes=15)
                    output += f"{date}: {start_time.strftime('%H:%M')} - {end_time.strftime('%H:%M')}\n"
                output += "\n"  # Добавляем пустую строку для разделения расписаний разных врачей

            bot.send_message(message.chat.id, output)
            clear_patient_messages(message.chat.id)

        else:
            bot.reply_to(message, "Выбранный Вами врач не существует, попробуйте выбрать снова")

    cases = {
        0: appointment_schedule_num0,
        1: appointment_schedule_num1,
    }
    func = cases.get(appointment_schedule_num, lambda *args: print("Неизвестный случай1"))
    func(message, chat_messages)
