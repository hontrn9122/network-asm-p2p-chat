import sqlite3
import json


def load_data(filename):
    with open(filename, 'r') as sql_file:
        sql = sql_file.read()
    conn = sqlite3.connect('user.db')
    database = conn.cursor()
    database.executescript(sql)
    conn.commit()
    conn.close()


def get_user(database, userid):
    user = database.execute(
        f"SELECT * FROM account WHERE userid='{userid}'")
    user = user.fetchone()
    return user


def get_friend(database, userid):
    friends = database.execute(f"SELECT * FROM friend WHERE userid='{userid}'")
    if friends:
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


def delete_friend(database, userid, friendid):
    database.execute(
        f"DELETE FROM friend WHERE userid='{userid}' AND friendid='{friendid}'")
    database.commit()
    database.execute(
        f"DELETE FROM friend WHERE userid='{friendid}' AND friendid='{userid}'")
    database.commit()


def add_friend(database, userid, friendid):
    database.execute(
        f"INSERT INTO friend VALUES('{userid}','{friendid}')"
    )
    database.commit()
    database.execute(
        f"INSERT INTO friend VALUES('{friendid}','{userid}')"
    )
    database.commit()
