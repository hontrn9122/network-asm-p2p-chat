import sqlite3


def load_data(filename):
    with open(filename, 'r') as sql_file:
        sql = sql_file.read()
    conn = sqlite3.connect('user.db')
    database = conn.cursor()
    database.executescript(sql)
    conn.commit()
    conn.close()


def auth_login(database, userid):
    user = database.execute(
        f"SELECT * FROM account WHERE userid='{userid}'")
    user = user.fetchone()
    if user:
        return user
    return None


def get_friend(database, userid):
    friends = database.execute(
        f"SELECT * FROM friend WHERE userid='{userid}'")
    if friends is not None:
        return friends
    return None


def check_email(database, email):
    user = database.execute(
        f"SELECT * FROM account WHERE email='{email}'")
    if user.fetchone():
        return True
    return False


def check_id(database, userid):
    user = database.execute(
        f"SELECT * FROM account WHERE userid='{userid}'")
    if user.fetchone():
        return True
    return False


def check_infor(database, userid, email):
    user = database.execute(
        f"SELECT * FROM account WHERE userid='{userid}' AND email='{email}'")
    if user.fetchone():
        return True
    return False


def register_account(database, userid, password, email):
    database.execute(
        f"INSERT INTO account VALUES ('{userid}', '{password}', '{email}')")
    database.commit()


def update_password(database, userid, password):
    database.execute(
        f"UPDATE account SET password='{password}' WHERE userid='{userid}'")
    database.commit()
