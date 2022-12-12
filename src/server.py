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
        print(client_address)
        client_thread = threading.Thread(target=verify_account, args=(client_socket, client_address,))
        client_thread.start()
    server_socket.close()


def verify_account(client_socket, client_address):
    database = sqlite3.connect('user.db')
    flag, message = client_socket.recv(BYTESIZE).decode(ENCODER).split(' ')
    print(flag, message)
    if flag == 'LOGIN':
        li_userid, li_password = message.split(':')
        if login(client_socket, li_userid, li_password, database):
            client_name_list.append(li_userid)
            client_address_list.append(client_address)
            client_socket_list.append(client_socket)
            service(client_socket, li_userid, database)
        return
    elif flag == 'REGISTER':
        reg_userid, reg_email, reg_password = message.split(':')
        if register(client_socket, reg_userid,
                    reg_password, reg_email, database):
            client_name_list.append(reg_userid)
            client_address_list.append(client_address)
            client_socket_list.append(client_socket)
            service(client_socket, reg_userid, database)
        return
    elif flag == 'FORGOTPASS':
        fp_userid, fp_email, new_password = message.split(':')
        if forgot_pass(client_socket, fp_userid, new_password, fp_email, database):
            client_name_list.append(fp_userid)
            client_address_list.append(client_address)
            client_socket_list.append(client_socket)
            service(client_socket, fp_userid, database)
        return


def get_friend_ids(friends):
    friend_name = ' '
    friend_ip = ' '
    friend_port = ' '
    if friends:
        for friend in friends:
            ip = 'NULL'
            port = 'NULL'
            if friend[1] in client_name_list:
                index = client_name_list.index(friend[1])
                ip, port = client_address_list[index]
            friend_name += friend[1] + ' '
            friend_ip += str(ip) + ' '
            friend_port += str(port) + ' '
    return friend_name, friend_ip, friend_port


def login(client_socket, li_userid, li_password, database):
    user = get_user(database, li_userid)
    if user:
        userid, password, email = user
        if password == li_password:
            send_message(client_socket, 'SUCCESS')
            send_message(client_socket, email)

            friends = get_friend(database, userid)
            friend_name, friend_ip, friend_port = get_friend_ids(friends)
            send_message(client_socket, friend_name)
            send_message(client_socket, friend_ip)
            send_message(client_socket, friend_port)
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
    return True


def friend_request():
    pass


def accept_friend_request():
    pass


def reject_friend_request():
    pass


def find_user():
    pass


def send_message(client_socket, message):
    time.sleep(0.01)
    client_socket.send(message.encode(ENCODER))


def service(client_socket, userid, database):
    while True:
        try:
            flag, message = client_socket.recv(BYTESIZE).decode(ENCODER).split(' ')
            print(flag, message)
            if flag == 'UNFRIEND':
                delete_friend(database, userid, message)
            elif flag == 'FIND':
                if get_user(database, message):
                    if message in client_name_list:
                        client_socket.send("FOUND_ONLINE".encode(ENCODER))
                    else:
                        client_socket.send("FOUND_OFFLINE".encode(ENCODER))
                else:
                    client_socket.send("NOTFOUND".encode(ENCODER))
            elif flag == 'REQUEST':
                tmp_socket = client_socket_list[client_name_list.index(message)]


        except:
            print('close')
            database.close()
            client_socket.close()
            break


if __name__ == '__main__':
    load_data('user.sql')
    server()
