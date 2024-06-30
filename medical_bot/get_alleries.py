import telebot
import os
from db_connection import create_db_connection

BOT_TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN, threaded=False)


def command_get_allergies(message):
    chat_id = message.chat.id
    conn = create_db_connection()
    cur = conn.cursor()
    query = f'''select at.name as atname, a.allergen, rt.name as rtname  from "Allergies" as a
    join "Allergies_types" as at on at.id = a.allergy_type_id
    join "Reaction_type" rt on a.reaction_id = rt.id
    where patient_id = (select id from "Patient" where chat_id = '{chat_id}')'''
    cur.execute(query)
    results = cur.fetchall()
    cur.close()
    conn.close()
    if len(results) != 0:
        mess = 'Ваши аллергии:\n\n'
        for row in results:
            type_name = row[0]
            a_name = row[1]
            react_name = row[2]
            mess += f"Аллерген: {a_name}\n" \
                    f"Тип аллергии: {type_name}\n" \
                    f"Реакция на аллергию: {react_name}\n\n"
        bot.send_message(message.chat.id, mess)
    else:
        bot.send_message(message.chat.id, "У вас нет добавленных аллергий")
