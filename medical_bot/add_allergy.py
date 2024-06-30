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


def command_add_allergy(message):
    chat_messages = []
    chat_id = message.chat.id
    print("Отправлено в очистку сообщений")
    clear_patient_messages(chat_id)
    info_num = 0
    add_allergy_switcher(int(info_num), message, chat_messages)


def get_allergies_types():
    conn = create_db_connection()
    cur = conn.cursor()
    query = f'''select name from "Allergies_types"'''
    cur.execute(query)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


def get_reactions():
    conn = create_db_connection()
    cur = conn.cursor()
    query = f'''select name from "Reaction_type"'''
    cur.execute(query)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


def add_new_allergy(message, allergen, allergy_type, reaction):
    chat_id = str(message.chat.id)
    conn = create_db_connection()
    cur = conn.cursor()
    query = f'''insert into "Allergies" (allergy_type_id, allergen, reaction_id, patient_id) 
    VALUES ((select id from "Allergies_types" where name = '{allergy_type}'),
    '{allergen}', (select id from "Reaction_type" where name = '{reaction}'), 
    (select id from "Patient" where chat_id = '{chat_id}'))'''
    cur.execute(query)
    if cur.rowcount > 0:
        print("INSERT успешно выполнен.")
    else:
        print("Ошибка при выполнении INSERT.")
    conn.commit()
    cur.close()
    conn.close()


def add_allergy_switcher(add_allergy_num, message, chat_messages):
    def add_allergy_num0(message, chat_messages):
        chat_id = message.chat.id
        text = message.text
        column_name = 'command'
        print("Отправлено в добавление сообщения")
        add_message(text, column_name, chat_id)
        bot.send_message(message.chat.id, "Введите название аллергена.")

    def add_allergy_num1(message, chat_messages):
        allergen_name = message.text
        add_message(allergen_name, 'msg1', message.chat.id)
        rows = get_allergies_types()
        if len(rows) != 0:
            buttons = []
            for row in rows:
                buttons.append(row[0])
            keyboard = create_keyboard(buttons)
            bot.send_message(message.chat.id, "Выберите подходящий вид аллергии.", reply_markup=keyboard)
        else:
            print('Не найдены типы аллергий в блоке add_allergy_num1')

    def add_allergy_num2(message, chat_messages):
        allergy_type = message.text
        rows = get_allergies_types()
        if len(rows) != 0:
            allergy_types = []
            for row in rows:
                allergy_types.append(row[0])
            if allergy_type in allergy_types:
                add_message(allergy_type, 'msg2', message.chat.id)
                rows = get_reactions()
                if len(rows) != 0:
                    buttons = []
                    for row in rows:
                        buttons.append(row[0])
                    keyboard = create_keyboard(buttons)
                    bot.send_message(message.chat.id, "Выберите подходящую реакцию на аллергию.", reply_markup=keyboard)
                else:
                    print('Не найдены типы реакции в блоке add_allergy_num2')
            else:
                keyboard = create_keyboard(allergy_types)
                bot.send_message(message.chat.id, "Выбранный вид аллергии не соответствует существующим.\n"
                                                  "Выберите подходящий вид аллергии.", reply_markup=keyboard)
        else:
            print('Не найдены типы аллергий в блоке add_allergy_num1')

    def add_allergy_num3(message, chat_messages):
        reaction = message.text
        rows = get_reactions()
        if len(rows) != 0:
            reactions = []
            for row in rows:
                reactions.append(row[0])
            if reaction in reactions:
                allergen = chat_messages[1]
                allergy_type = chat_messages[2]
                add_new_allergy(message, allergen, allergy_type, reaction)
                bot.send_message(message.chat.id, 'Аллергия успешно добавлена.')
                clear_patient_messages(message.chat.id)
            else:
                keyboard = create_keyboard(reactions)
                bot.send_message(message.chat.id, "Выбранная реакция не соответствует существующим.\n"
                                                  "Выберите подходящую реакцию.", reply_markup=keyboard)
        else:
            print('Не найдены типы реакции в блоке add_allergy_num3')

    cases = {
        0: add_allergy_num0,
        1: add_allergy_num1,
        2: add_allergy_num2,
        3: add_allergy_num3
    }
    func = cases.get(add_allergy_num, lambda *args: print("Неизвестный случай1"))
    func(message, chat_messages)
