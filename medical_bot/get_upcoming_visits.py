import telebot
import os
from datetime import datetime
from db_connection import create_db_connection
from chat_messages import clear_patient_messages

BOT_TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN, threaded=False)



def command_get_upcoming_visits(message):
    chat_id = str(message.chat.id)
    conn = create_db_connection()
    cur = conn.cursor()
    query = f'''SELECT d.name AS doctor_name, s.name AS specialization_name, a.appointment_time, a.appointment_date, o.office_number
            FROM "Appointments" AS a
            JOIN "Doctor" AS d ON a.doctor_id = d.id
            JOIN "Specialization" AS s ON a.specialization_id = s.id
            join "Doctor_offices" o on o.id = a.doctor_offices_id
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
    if len(rows) == 0:
        bot.send_message(message.chat.id, "У вас нет записей на прием.")
    else:
        mess = ''
        bot.send_message(message.chat.id, "Ваши записи на прием:")
        counter = 0
        for row in rows:
            doc_name = row[0]
            spec = row[1]
            time = row[2].strftime("%H:%M")
            date = row[3].strftime("%d.%m.%Y")
            office_number = row[4]
            mess += f"{date} {time} \nКабинет: {office_number}\n{spec}: {doc_name}\n\n"
            counter += 1
            if counter % 10 == 0:
                bot.send_message(message.chat.id, mess)
                mess = ''
        if counter % 10 != 0:
            bot.send_message(message.chat.id, mess)
    clear_patient_messages(message.chat.id)
