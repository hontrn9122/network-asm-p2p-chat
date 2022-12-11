import tkinter
import socket
import threading
import os
import json
import time
import sqlite3
from db import *
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
friend_list = {}

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
    database = sqlite3.connect('user.db')
    flag, message = client_socket.recv(BYTESIZE).decode(ENCODER).split(' ')
    print(flag, message)
    if flag == 'LOGIN':
        li_userid, li_password = message.split(':')
        if login(client_socket, li_userid, li_password, database):
            client_name_list.append(li_userid)
            client_socket_list.append(client_address)
            service(client_socket, li_userid, database)
        return
    elif flag == 'REGISTER':
        reg_userid, reg_email, reg_password = message.split(':')
        if register(client_socket, reg_userid,
                    reg_password, reg_email, database):
            client_name_list.append(reg_userid)
            client_socket_list.append(client_address)
            service(client_socket, reg_userid, database)
        return
    elif flag == 'FORGOTPASS':
        fp_userid, fp_email, new_password = message.split(':')
        if forgot_pass(client_socket, fp_userid, new_password, fp_email, database):
            client_name_list.append(fp_userid)
            client_socket_list.append(client_address)
            service(client_socket, fp_userid, database)
        return


def get_friend_ids(friends):
    friend_name = ' '
    friend_ip = ' '
    friend_port = ' '

    if friends is not None:
        for friend in friends:
            friend_ids = friend[1].split(' ')
            for friend_id in friend_ids:
                ip = 'NULL'
                port = 'NULL'
                if friend_id in client_name_list:
                    index = client_name_list.index(friend_id)
                    ip, port = client_socket_list[index]
                friend_name += friend_id + ' '
                friend_ip += str(ip) + ' '
                friend_port += str(port) + ' '
    return friend_name, friend_ip, friend_port


def login(client_socket, li_userid, li_password, database):
    user = auth_login(database, li_userid)
    if user is not None:
        userid, password, email = user
        if password == li_password:
            send_message(client_socket, 'SUCCESS')
            send_message(client_socket, email)

            friends = get_friend(database, userid)
            friend_name, friend_ip, friend_port = get_friend_ids(friends)
            friend_list[li_userid] = friend_name
            send_message(client_socket, friend_name)
            send_message(client_socket, friend_ip)
            send_message(client_socket, friend_port)
            return True
    send_message(client_socket, 'FAIL')
    return False


def register(client_socket, userid, password, email, database):
    if check_info(database, userid, email):
        send_message(client_socket, 'FAIL')
        return False
    register_account(database, userid, password, email)
    send_message(client_socket, 'SUCCESS')
    return True


def forgot_pass(client_socket, fp_userid, new_password, fp_email, database):
    if check_id(database, fp_userid):
        send_message(client_socket, 'FAIL_USERID')
        return False
    if check_email(database, fp_userid, fp_email):
        send_message(client_socket, 'FAIL_EMAIL')
        return False
    update_password(database, fp_userid, new_password)
    send_message(client_socket, 'SUCCESS')
    return True


def friend_request():
    pass


def accept_friend_request():
    pass


def reject_friend_request():
    pass


def unfriend(userid, message, database):
    temp = friend_list[userid].strip().split(' ')
    if message in temp:
        temp.remove(message)
        temp = str.join(' ', temp)
        friend_list[userid] = temp
        if len(temp) != 0:
            update_friend_list(database, userid, temp)
        else:
            delete_friend_list(database, userid)
        unfriend(message, userid, database)
        return True
    return False


def find_user():
    pass


def send_message(client_socket, message):
    time.sleep(0.01)
    client_socket.send(message.encode(ENCODER))


def service(client_socket, userid, database):
    try:
        flag, message = client_socket.recv(BYTESIZE).decode(ENCODER).split(' ')
        send_message(client_socket, 'FRIEND_LIST_UPDATE')

        if flag == 'UNFRIEND':
            if unfriend(userid, message, database):
                send_message(client_socket, 'FRIEND_LIST_UPDATE')
                send_message(client_socket, friend_list[userid])
            else:
                print('FAIL')
        elif flag == 'FIND':
            pass
        elif flag == 'REQUEST':
            pass
    except:
        client_socket.close()


if __name__ == '__main__':
    load_data('user.sql')
    server()
