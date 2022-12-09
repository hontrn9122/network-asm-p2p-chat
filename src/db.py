import json


class user:
    def __init__(self, user_id, password, email, friend_list):
        self.user_id = user_id
        self.password = password
        self.email = email
        self.friend_list = friend_list


user_db = {}
online_users = []


def load_data():
    file = open('user.json')
    users = json.load(file)
    for user_info in users["user"]:
        user_info = json.dumps(user_info)
        user_info = json.loads(user_info)

        username = user_info["username"]
        password = user_info["password"]
        email = user_info["email"]
        friend_list = user_info["friend_list"]

        tmp = user(username, password, email, friend_list)
        user_db[username] = tmp


def save_data():
    pass


def add_user(username, password):
    user_db[username] = user(username, password)
