import tkinter, socket, threading, os, json
from tkinter import *
from tkinter import messagebox
from theme import *
from tkinter.messagebox import askyesno, showerror
from tkinter import filedialog

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
    'huyhoang' : {
        'email' : 'huy@gamil.com',
        'password': '123456',
        'friend_list': [],
    }
}

# Create a server socket using TCP protocol
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOSTNAME, PORT))
server_socket.listen()

# Connecting client
def connect_client():
    while True:
        client_socket, client_address = server_socket.accept()
        client_thread = threading.Thread(target=verify_account, args=(client_socket, client_address,))
        client_thread.start()


def verify_account(client_socket, client_address):
    flag, message = client_socket.recv(BYTESIZE).decode(ENCODER)
    if flag == 'LOGIN':
        userId, password = message.split(':')
        if userId not in user_account_list:
            client_socket.send('FAIL'.encode(ENCODER))
            return
        elif password == user_account_list[userId]['password']:
            client_socket.send(user_account_list[userId]['email'].encode(ENCODER))
            friend_name = json.dumps(user_account_list[userId]['friend_list'])
            if friend_name == '[]':
                client_socket.send('NULL'.encode(ENCODER))
            else:
                client_socket.send(friend_name.encode(ENCODER))
            client_socket.send('NULL'.encode(ENCODER))
            client_socket.send('NULL'.encode(ENCODER))



    elif flag == "REGISTER":
        pass
    elif flag == "FORGOTPASS":
        pass

# def recieve_message(client_socket):
#     try:
#         flag, message = client_socket.recv(BYTESIZE).decode(ENCODER)
#         if flag == 'LOGIN':
#             pass
#         if
#     except:
#         pass

connect_client()