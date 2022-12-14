import json
import socket
import threading
import time
from db import *

# Defining constant
HOSTNAME = 'localhost'
PORT = 50000
ENCODER = 'utf-8'
BYTESIZE = 1024

# Manage online client
client_socket_list = []
client_address_list = []
client_name_list = []

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
    # server_socket.close()


# Account management ----------------------------
def verify_account(client_socket, client_address):
    database = sqlite3.connect('user.db')
    flag, message = client_socket.recv(BYTESIZE).decode(ENCODER).split(' ')
    print(flag, message)
    if flag == 'LOGIN':
        li_userid, li_password = message.split(':')
        if login(client_socket, li_userid, li_password, database):
            client_name_list.append(li_userid)
            client_socket_list.append(client_socket)
            ip, port = client_socket.recv(BYTESIZE).decode(ENCODER).split(':')
            client_address_list.append((ip, int(port)))
            service(client_socket, li_userid, database)
        else:
            database.close()
            client_socket.close()
    elif flag == 'REGISTER':
        reg_userid, reg_email, reg_password = message.split(':')
        if register(client_socket, reg_userid, reg_password, reg_email, database):
            client_name_list.append(reg_userid)
            client_socket_list.append(client_socket)
            ip, port = client_socket.recv(BYTESIZE).decode(ENCODER).split(':')
            client_address_list.append((ip, int(port)))
            service(client_socket, reg_userid, database)
        else:
            database.close()
            client_socket.close()
    elif flag == 'FORGOTPASS':
        fp_userid, fp_email, new_password = message.split(':')
        if forgot_pass(client_socket, fp_userid, new_password, fp_email, database):
            client_name_list.append(fp_userid)
            client_socket_list.append(client_socket)
            ip, port = client_socket.recv(BYTESIZE).decode(ENCODER).split(':')
            client_address_list.append((ip, int(port)))
            service(client_socket, fp_userid, database)
        else:
            database.close()
            client_socket.close()


def login(client_socket, li_userid, li_password, database):
    user = get_user(database, li_userid)
    if user:
        userid, password, email = user
        if password == li_password:
            send_message(client_socket, 'SUCCESS')
            send_message(client_socket, email)
            send_list_friend(client_socket, database, li_userid)
            return True
    send_message(client_socket, 'FAIL')
    return False


def register(client_socket, userid, password, email, database):
    if check_id(database, userid):
        send_message(client_socket, 'FAIL_USERID')
        return False
    if check_email(database, email):
        send_message(client_socket, 'FAIL_EMAIL')
        return False
    register_account(database, userid, password, email)
    send_message(client_socket, 'SUCCESS')
    return True


def forgot_pass(client_socket, fp_userid, new_password, fp_email, database):
    if not check_infor(database, fp_userid, fp_email):
        send_message(client_socket, 'FAIL')
        return False
    update_password(database, fp_userid, new_password)
    send_message(client_socket, 'SUCCESS')
    send_list_friend(client_socket, database, fp_userid)
    return True


# Listen Client Message --------------------------------------------
def service(client_socket, userid, database):
    update_personal_status(database, userid, "online")
    while True:
        try:
            flag, message = client_socket.recv(BYTESIZE).decode(ENCODER).split(' ', 1)
            print(flag, message)
            if flag == 'UNFRIEND':
                delete_friend(database, userid, message)
            elif flag == 'FIND':
                user = get_user(database, message)
                if user and user[0] != userid:
                    if message in client_name_list:
                        client_socket.send("FOUND_ONLINE".encode(ENCODER))
                    else:
                        client_socket.send("FOUND_OFFLINE".encode(ENCODER))
                else:
                    client_socket.send("NOTFOUND".encode(ENCODER))
            elif flag == 'REQUEST':
                tmp_socket = client_socket_list[client_name_list.index(message)]
                send_message(tmp_socket, 'FRIEND_REQUEST')
                send_message(tmp_socket, userid)
            elif flag == 'ACCEPT_FRIEND':
                add_friend(database, userid, message)
                client_socket.send("FRIEND_LIST_UPDATE".encode(ENCODER))
                send_list_friend(client_socket, database, userid)

                tmp_socket = client_socket_list[client_name_list.index(message)]
                tmp_socket.send("FRIEND_LIST_UPDATE".encode(ENCODER))
                send_list_friend(tmp_socket, database, message)

                client_socket.send("DEL_TIMEOUT_REQUEST".encode(ENCODER))
                send_message(client_socket, message)
            elif flag == 'REFUSE_FRIEND':
                tmp_socket = client_socket_list[client_name_list.index(message)]
                send_message(tmp_socket, 'REQUEST_DENIED')
                send_message(tmp_socket, userid)
                client_socket.send("DEL_TIMEOUT_REQUEST".encode(ENCODER))
                send_message(client_socket, message)
            elif flag == 'FRIEND_REQUEST_TIMEOUT':
                list_timeout = json.loads(message)
                print(list_timeout)
                for user in list_timeout:
                    if user in client_name_list:
                        tmp_socket = client_socket_list[client_name_list.index(user)]
                        send_message(tmp_socket, "REQUEST_TIMEOUT")
                        send_message(tmp_socket, userid)
        except:
            update_personal_status(database, userid, "offline")
            index = client_socket_list.index(client_socket)
            client_socket_list.remove(client_socket)
            client_name_list.remove(client_name_list[index])
            client_address_list.remove(client_address_list[index])
            print(f'close + {userid}')
            database.close()
            client_socket.close()
            break


# Support Function -------------------------------------
def send_message(client_socket, message):
    time.sleep(0.01)
    client_socket.send(message.encode(ENCODER))


def get_friend_ids(friends):
    friend_name = ''
    friend_ip = ''
    friend_port = ''
    friends = friends.fetchall()
    if len(friends) != 0:
        for friend in friends:
            ip = 'NULL'
            port = 'NULL'
            if friend[1] in client_name_list:
                index = client_name_list.index(friend[1])
                ip, port = client_address_list[index]
            friend_name += friend[1] + ' '
            friend_ip += str(ip) + ' '
            friend_port += str(port) + ' '
    else:
        friend_name = "NULL"
        friend_ip = "NULL"
        friend_port = "NULL"
    return friend_name.strip(), friend_ip.strip(), friend_port.strip()


def send_list_friend(client_socket, database, userid):
    friends = get_friend(database, userid)
    friend_name, friend_ip, friend_port = get_friend_ids(friends)
    send_message(client_socket, friend_name)
    send_message(client_socket, friend_ip)
    send_message(client_socket, friend_port)


def update_personal_status(database, userid, status):
    friends = get_friend(database, userid).fetchall()
    for friend in friends:
        if friend[1] in client_name_list:
            tmp_socket = client_socket_list[client_name_list.index(friend[1])]
            send_message(tmp_socket, "UPDATE_FRIEND_STATUS")
            send_message(tmp_socket, userid)
            ip, port = client_address_list[client_name_list.index(userid)]
            if status == "offline":
                ip = "NULL"
                port = "NULL"
            send_message(tmp_socket, f"{ip}:{port}")


# Run server ------------------------------------
if __name__ == '__main__':
    load_data('user.sql')
    server()
