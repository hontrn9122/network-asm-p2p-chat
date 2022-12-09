class user:
    def __init__(self, user_id, password, email):
        self.user_id = user_id
        self.password = password
        self.email = email
        self.friend_list = []


user_db = {}
online_users = []
usernames = ['guest0', 'guest1', 'guest2', 'guest3', 'guest4',
             'guest5', 'guest6', 'guest7', 'guest8', 'guest9']


def load_data():
    for username in usernames:
        tmp = user(username, username)
        user_db[username] = tmp


def add_user(username, password):
    user_db[username] = user(username, password)
