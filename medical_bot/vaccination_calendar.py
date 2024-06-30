import telebot
import os
from datetime import datetime
from dateutil.relativedelta import relativedelta
from db_connection import create_db_connection

BOT_TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN, threaded=False)


def command_vaccination_calendar(message):
    chat_id = message.chat.id
    conn = create_db_connection()
    cur = conn.cursor()
    query = f'''select v.name, p.date_of_vaccination, v.frequency from "Patient_vaccinations" as p
                join "Vaccination_types" as v on p.vaccination_type_id = v.id
                where p.patient_id = (select id from "Patient" where chat_id = '{chat_id}')'''
    cur.execute(query)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    if len(rows) != 0:
        mess = 'Ваши прививки\n\n'
        for row in rows:
            name = row[0]
            date_of_vaccination = row[1]
            frequency = row[2] if row[2] is not None else ""
            date_obj = date_of_vaccination
            date_of_vaccination_str = date_obj.strftime('%d.%m.%Y')
            if frequency != '':
                new_date_obj = date_obj + relativedelta(years=frequency)
                next_date_of_vaccination = new_date_obj.strftime('%d.%m.%Y')
                mess += f"Название: {name}\n" \
                        f"Дата прививки: {date_of_vaccination_str}\n" \
                        f"Дата следующей прививки: {next_date_of_vaccination}\n\n"
            else:
                mess += f"Название: {name}\n" \
                        f"Дата прививки: {date_of_vaccination_str}\n\n"
        bot.send_message(message.chat.id, mess)
    else:
        bot.send_message(message.chat.id, "У вас нет прививок")
