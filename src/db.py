import sqlite3

conn = sqlite3.connect('user.db')


def load_data(filename):
    with open(filename, 'r') as sql_file:
        sql = sql_file.read()
    cs = conn.cursor()
    cs.executescript(sql)
    conn.commit()
    conn.close()


if __name__ == '__main__':
    load_data('user.sql')
