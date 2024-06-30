import telebot
import os
from db_connection import create_db_connection

BOT_TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN, threaded=False)


def command_get_medications(message):
    chat_id = message.chat.id
    conn = create_db_connection()
    cur = conn.cursor()
    query = f'''select name, start_date, end_date from "Taken_medications"
                where patient_id = (select id from "Patient" where chat_id = '{chat_id}')'''
    cur.execute(query)
    results = cur.fetchall()
    cur.close()
    conn.close()
    if len(results) != 0:
        mess = 'Ваши принимаемые медикаменты:\n\n'
        for row in results:
            name = row[0]
            start_date = row[1].strftime("%d.%m.%Y")
            end_date = row[2].strftime("%d.%m.%Y") if row[2] is not None else "по настоящее время"
            mess += f"Название медикамента: {name}\n" \
                    f"Дата начала приема: {start_date}\n" \
                    f"Дата конца приема: {end_date}\n\n"
        bot.send_message(message.chat.id, mess)
    else:
        bot.send_message(message.chat.id, "У вас нет добавленных принимаемых медикаментов")
