import sqlite3


def open_db():
    """Создание базы данных"""
    connect = sqlite3.connect('db.sqlite3')
    cursor = connect.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS bad_word_increment(id INTEGER PRIMARY KEY,
                                                                     user_id INT,
                                                                     counter INT 
                                                                     )""")
    cursor.close()
    connect.close()


def insert_answer(user_id: int, count: int):
    """Добавление новых записей"""
    connect = sqlite3.connect('db.sqlite3')
    curs = connect.cursor()
    curs.execute("""SELECT * FROM bad_word_increment WHERE user_id = (?)""", (user_id,))
    request_db = curs.fetchall()
    if request_db:
        curs.execute("""UPDATE bad_word_increment SET counter = (?) WHERE user_id = (?)""",
                     (request_db[0][-1] + count, user_id,))
    else:
        curs.execute("""INSERT INTO bad_word_increment(user_id, counter) VALUES (?,?)""",
                    (user_id, count))
    connect.commit()
    curs.close()
    connect.close()

def counter():

    connect = sqlite3.connect('db.sqlite3')
    curs = connect.cursor()
    curs.execute("""SELECT * FROM bad_word_increment ORDER BY counter DESC """)
    result = curs.fetchall()
    curs.close()
    connect.close()
    return result


