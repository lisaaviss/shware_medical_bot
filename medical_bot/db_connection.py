import psycopg2
access_token = ''

def set_access_token(token):
    global access_token
    access_token = token

def create_db_connection():
    conn = psycopg2.connect(
        database="************",
        user="********",
        password=access_token,
        port=6432,
        host="************",
        sslmode="require"
    )
    if not conn.closed:
        print("Соединение успешно установлено")
        return conn
    else:
        print("Ошибка: соединение не установлено")