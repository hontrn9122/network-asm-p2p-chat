import tkinter
import socket
import threading
import os
import json
import time
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
        client_thread = threading.Thread(
            target=verify_account, args=(client_socket, client_address,))
        client_thread.start()


def verify_account(client_socket, client_address):
    flag, message = client_socket.recv(BYTESIZE).decode(ENCODER).split(' ')
    if flag == 'LOGIN':
        userid, password = message.split(':')
        if login(client_socket, userid, password):
            client_name_list.append(userid)
            client_name_list.append(client_address)
            service(client_socket)
        else:
            return
    elif flag == "REGISTER":
        userid, password = message.split(':')
    elif flag == "FORGOTPASS":
        pass


def login(client_socket, userid, password):
    if userid not in user_account_list:
        client_socket.send('FAIL'.encode(ENCODER))
    elif password == user_account_list[userid]['password']:
        client_socket.send('SUCCESS'.encode(ENCODER))
        time.sleep(0.01)
        client_socket.send(
            (user_account_list[userid]['email']).encode(ENCODER))
        time.sleep(0.01)
        friend_name = json.dumps(user_account_list[userid]['friend_list'])
        if friend_name == '[]':
            client_socket.send('NULL'.encode(ENCODER))
        else:
            client_socket.send(friend_name.encode(ENCODER))
        time.sleep(0.01)
        client_socket.send('NULL'.encode(ENCODER))
        time.sleep(0.01)
        client_socket.send('NULL'.encode(ENCODER))
        return True
    return False


def service(client_socket):
    try:
        flag, message = client_socket.recv(BYTESIZE).decode(ENCODER).split(' ')
        if flag == 'UNFRIEND':
            pass
        elif flag == 'FIND':
            pass
        elif flag == 'REQUEST':
            pass
    except:
        client_socket.close()


if __name__ == '__main__':
    server()
