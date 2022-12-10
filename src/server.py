import tkinter, socket, threading, os, json, time
import sqlite3
from tkinter import *
from tkinter import messagebox
from theme import *
from tkinter.messagebox import askyesno, showerror
from tkinter import filedialog
# database = sqlite3.connect('account.db')
# c = database.cursor()
# c.execute("""CREATE TABLE account (
#     userid text,
#     password text,
#     email text
# )""")
# c.execute("""CREATE TABLE friend (
#     userid text,
#     friendid text
# )""")
# c.execute("INSERT INTO account VAlUES ('hoang', '123', 'hoang@gmail.com')")
# # c.execute("INSERT INTO account VAlUES ('danh', '123789', 'danh@gmail.com')")
# # c.execute("INSERT INTO friend VAlUES ('huyhoang', 'danh')")
# # c.execute("INSERT INTO friend VAlUES ('danh', 'huyhoang')")
# database.commit()
# database.close()
# Defining constant
HOSTNAME = 'localhost'
PORT = 50000
ENCODER = 'utf-8'
BYTESIZE = 1024

# Manage online client
client_socket_list = []
client_name_list = []

# Manage user account and their friends
# Structure of User Account:
#  userId: {
#      password<string>,
#      email<string>,
#      friend_ip[],
#      friend_port[]
#  }
user_account_list = {
    "huyhoang": {
        "email": "huy@gmail.com",
        "password": "123456",
        "friend_list": [],
    }
}

# Create a server socket using TCP protocol
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOSTNAME, PORT))
server_socket.listen()


# Connecting client
def server():
    while True:
        client_socket, client_address = server_socket.accept()
        client_thread = threading.Thread(target=verify_account, args=(client_socket, client_address,))
        client_thread.start()


def verify_account(client_socket, client_address):
    database = sqlite3.connect('account.db')
    flag, message = client_socket.recv(BYTESIZE).decode(ENCODER).split(' ')
    if flag == 'LOGIN':
        userid, password = message.split(':')
        if login(client_socket, userid, password, database):
            client_name_list.append(userid)
            client_name_list.append(client_address)
            service(client_socket)
        else:
            client_socket.close()
            database.close()
            return
    elif flag == "REGISTER":
        pass
    elif flag == "FORGOTPASS":
        pass


def login(client_socket, userid, password, database):
    user = database.execute("SELECT * FROM account WHERE userid=?", (userid,))
    user = user.fetchone()
    if user:
        print(user)
        id, c_password, email = user
        if password == c_password:
            client_socket.send('SUCCESS'.encode(ENCODER))
            time.sleep(0.01)
            client_socket.send(email.encode(ENCODER))
            time.sleep(0.01)
            friends = database.execute("SELECT * FROM friend WHERE userid=?", (userid,))
            friend_name = ""
            friend_ip = ""
            friend_port = ""
            for friend in friends:
                ip = "NULL"
                port = "NULL"
                if friend[1] in client_name_list:
                    index = client_name_list[friend[1]]
                    ip, port = client_socket_list[index]
                friend_name += friend[1] + " "
                friend_ip += ip + " "
                friend_port += port + " "
            client_socket.send(friend_name.strip().encode(ENCODER))
            time.sleep(0.01)
            client_socket.send(friend_ip.strip().encode(ENCODER))
            time.sleep(0.01)
            client_socket.send(friend_port.strip().encode(ENCODER))
            return True
    client_socket.send('FAIL'.encode(ENCODER))
    return False


def service(client_socket):
    pass


if __name__ == '__main__':
    server()