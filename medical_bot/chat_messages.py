from db_connection import create_db_connection


def clear_patient_messages(int_chat_id):
    chat_id= str(int_chat_id)
    conn = create_db_connection()
    cur = conn.cursor()
    cur.execute(
        'select * from "Messages" '
        'where patient_id = (select id from "Patient" where chat_id = %(chat_id)s)',
        {"chat_id": chat_id})
    rows = cur.fetchall()
    if len(rows) == 0:
        print("Сообщений нет вообще, отправлено в добавление пациента")
        add_patient_presence(chat_id)
    else:
        cur.execute('update "Messages" set '
                    'command = null, '
                    'msg1 = null, '
                    'msg2 = null,'
                    'msg3 = null,'
                    'msg4 = null, '
                    'msg5 = null,'
                    'msg6 = null,'
                    'msg7 = null,'
                    'msg8 = null,'
                    'msg9 = null,'
                    'msg10 = null where patient_id = (SELECT id FROM "Patient" WHERE chat_id = %(chat_id)s)',
                    {"chat_id": chat_id})
        conn.commit()
        print("Чистка сообщений осуществлена")
    cur.close()
    conn.close()


def add_message(text, column_name, int_chat_id):
    chat_id = str(int_chat_id)
    conn = create_db_connection()
    cur = conn.cursor()
    query = f'''
        UPDATE "Messages" 
        SET {column_name} = '{text}' 
        WHERE patient_id = (SELECT id FROM "Patient" WHERE chat_id = '{chat_id}')
    '''
    cur.execute(query)
    conn.commit()
    print("Сообщение добавлено")
    cur.close()
    conn.close()


def add_patient_presence(int_chat_id):
    chat_id = str(int_chat_id)
    conn = create_db_connection()
    cur = conn.cursor()
    cur.execute('INSERT INTO "Messages" (patient_id) SELECT id FROM "Patient" WHERE chat_id = %(chat_id)s',
                {"chat_id": chat_id})
    conn.commit()
    print("Пациент добавлен")
    cur.close()
    conn.close()


def get_chat_messages(int_chat_id):
    chat_id = str(int_chat_id)
    chat_messages = []
    str(chat_id)
    conn = create_db_connection()
    cur = conn.cursor()
    cur.execute(
        'select * from "Messages" '
        'where patient_id = (select id from "Patient" where chat_id = %(chat_id)s)',
        {"chat_id": chat_id})
    rows = cur.fetchall()
    cur.close()
    conn.close()
    if len(rows) == 0:
        add_patient_presence(chat_id)
        print('Сообщений у данного перца нет')
        return chat_messages
    else:
        for i in range(2, len(rows[0])):
            if rows[0][i] is not None:
                chat_messages.append(rows[0][i])
        return chat_messages
