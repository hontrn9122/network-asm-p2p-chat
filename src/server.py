import json
import socket
import threading
import time
import rsa
from db import *

# Defining constant
HOSTNAME = 'localhost'
PORT = 50000
ENCODER = 'utf-8'
BYTESIZE = 1024
PUB_KEY, PRI_KEY = rsa.newkeys(1024)

# Manage online client
client_socket_list = []
client_address_list = []
client_name_list = []
client_public_key = []

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
    client_public = rsa.PublicKey.load_pkcs1(client_socket.recv(BYTESIZE))
    client_socket.send(PUB_KEY.save_pkcs1("PEM"))
    flag, message = rsa.decrypt(client_socket.recv(BYTESIZE), PRI_KEY).decode(ENCODER).split(' ')

    print(flag, message)
    if flag == 'LOGIN':
        li_userid, li_password = message.split(':')
        if login(client_socket, client_public, li_userid, li_password, database):
            client_name_list.append(li_userid)
            client_socket_list.append(client_socket)
            client_public_key.append(client_public)
            ip, port = rsa.decrypt(client_socket.recv(BYTESIZE), PRI_KEY).decode(ENCODER).split(':')
            client_address_list.append((ip, int(port)))
            service(client_socket, li_userid, database)
        else:
            database.close()
            client_socket.close()
    elif flag == 'REGISTER':
        reg_userid, reg_email, reg_password = message.split(':')
        if register(client_socket, client_public, reg_userid, reg_password, reg_email, database):
            client_name_list.append(reg_userid)
            client_socket_list.append(client_socket)
            ip, port = rsa.decrypt(client_socket.recv(BYTESIZE), PRI_KEY).decode(ENCODER).split(':')
            client_address_list.append((ip, int(port)))
            client_public_key.append(client_public)
            service(client_socket, reg_userid, database)
        else:
            database.close()
            client_socket.close()
    elif flag == 'FORGOTPASS':
        fp_userid, fp_email, new_password = message.split(':')
        if forgot_pass(client_socket, client_public, fp_userid, new_password, fp_email, database):
            client_name_list.append(fp_userid)
            client_socket_list.append(client_socket)
            ip, port = rsa.decrypt(client_socket.recv(BYTESIZE), PRI_KEY).decode(ENCODER).split(':')
            client_address_list.append((ip, int(port)))
            client_public_key.append(client_public)
            service(client_socket, fp_userid, database)
        else:
            database.close()
            client_socket.close()


def login(client_socket, li_public, li_userid, li_password, database):
    user = get_user(database, li_userid)
    if user:
        userid, password, email = user
        if password == li_password:
            send_message(client_socket, li_public, 'SUCCESS')
            send_message(client_socket, li_public, email)
            send_list_friend(client_socket, li_public, database, li_userid)
            return True
    send_message(client_socket, li_public, 'FAIL')
    return False


def register(client_socket, client_public, userid, password, email, database):
    if check_id(database, userid):
        send_message(client_socket, client_public, 'FAIL_USERID')
        return False
    if check_email(database, email):
        send_message(client_socket, client_public, 'FAIL_EMAIL')
        return False
    register_account(database, userid, password, email)
    send_message(client_socket, client_public, 'SUCCESS')
    return True


def forgot_pass(client_socket, client_public, fp_userid, new_password, fp_email, database):
    if not check_infor(database, fp_userid, fp_email):
        send_message(client_socket, client_public, 'FAIL')
        return False
    update_password(database, fp_userid, new_password)
    send_message(client_socket, client_public, 'SUCCESS')
    send_list_friend(client_socket, client_public, database, fp_userid)
    return True


# Listen Client Message --------------------------------------------
def service(client_socket, userid, database):
    update_personal_status(database, userid, "online")
    client_idx = client_name_list.index(userid)
    while True:
        try:
            flag, message = rsa.decrypt(client_socket.recv(BYTESIZE), PRI_KEY).decode(ENCODER).split(' ', 1)
            print(flag, message)
            if flag == 'UNFRIEND':
                delete_friend(database, userid, message)
            elif flag == 'FIND':
                user = get_user(database, message)
                if user and user[0] != userid:
                    if message in client_name_list:
                        client_socket.send(rsa.encrypt("FOUND_ONLINE".encode(ENCODER), client_public_key[client_idx]))
                    else:
                        client_socket.send(rsa.encrypt("FOUND_OFFLINE".encode(ENCODER), client_public_key[client_idx]))
                else:
                    client_socket.send(rsa.encrypt("NOTFOUND".encode(ENCODER), client_public_key[client_idx]))
            elif flag == 'REQUEST':
                friend_idx = client_name_list.index(message)
                tmp_socket = client_socket_list[friend_idx]
                tmp_pub_key = client_public_key[friend_idx]
                send_message(tmp_socket, tmp_pub_key, 'FRIEND_REQUEST')
                send_message(tmp_socket, tmp_pub_key, userid)
            elif flag == 'ACCEPT_FRIEND':
                add_friend(database, userid, message)

                client_socket.send(rsa.encrypt("FRIEND_LIST_UPDATE".encode(ENCODER), client_public_key[client_idx]))
                send_list_friend(client_socket, client_public_key[client_idx], database, userid)

                tmp_idx = client_name_list.index(message)
                tmp_socket = client_socket_list[tmp_idx]
                tmp_pub_key = client_public_key[tmp_idx]
                tmp_socket.send(rsa.encrypt("FRIEND_LIST_UPDATE".encode(ENCODER), tmp_pub_key))
                send_list_friend(tmp_socket, tmp_pub_key, database, message)

                client_socket.send(rsa.encrypt("DEL_TIMEOUT_REQUEST".encode(ENCODER), client_public_key[client_idx]))
                send_message(client_socket, client_public_key[client_idx], message)
            elif flag == 'REFUSE_FRIEND':
                tmp_idx = client_name_list.index(message)
                tmp_socket = client_socket_list[tmp_idx]
                tmp_pub_key = client_public_key[tmp_idx]
                send_message(tmp_socket, tmp_pub_key, 'REQUEST_DENIED')
                send_message(tmp_socket, tmp_pub_key, userid)
                client_socket.send(rsa.encrypt("DEL_TIMEOUT_REQUEST".encode(ENCODER), client_public_key[client_idx]))
                send_message(client_socket, client_public_key[client_idx], message)
            elif flag == 'FRIEND_REQUEST_TIMEOUT':
                list_timeout = json.loads(message)
                print(list_timeout)
                for user in list_timeout:
                    if user in client_name_list:
                        tmp_idx = client_name_list.index(user)
                        tmp_socket = client_socket_list[tmp_idx]
                        tmp_pub_key = client_public_key[tmp_idx]
                        send_message(tmp_socket, tmp_pub_key, "REQUEST_TIMEOUT")
                        send_message(tmp_socket, tmp_pub_key, userid)
        except:
            update_personal_status(database, userid, "offline")
            index = client_socket_list.index(client_socket)
            client_socket_list.remove(client_socket)
            client_name_list.remove(client_name_list[index])
            client_address_list.remove(client_address_list[index])
            client_public_key.remove(client_public_key[index])
            print(f'close + {userid}')
            database.close()
            client_socket.close()
            break


# Support Function -------------------------------------
def send_message(client_socket, public_client, message):
    time.sleep(0.01)
    client_socket.send(rsa.encrypt(message.encode(ENCODER), public_client))

def send_key(client_socket, key):
    client_socket.send(key.save_pkcs1("PEM"))

def get_friend_ids(friends):
    friend_name = ''
    friend_ip = ''
    friend_port = ''
    friend_public_key = []
    friends = friends.fetchall()
    if len(friends) != 0:
        for friend in friends:
            ip = 'NULL'
            port = 'NULL'
            if friend[1] in client_name_list:
                index = client_name_list.index(friend[1])
                ip, port = client_address_list[index]
                friend_public_key.append(client_public_key[index])
            else:
                friend_public_key.append(None)
            friend_name += friend[1] + ' '
            friend_ip += str(ip) + ' '
            friend_port += str(port) + ' '
    else:
        friend_name = "NULL"
        friend_ip = "NULL"
        friend_port = "NULL"
        friend_public_key = []
    return friend_name.strip(), friend_ip.strip(), friend_port.strip(), friend_public_key


def send_list_friend(client_socket, public_client, database, userid):
    friends = get_friend(database, userid)
    friend_name, friend_ip, friend_port, friend_public_key = get_friend_ids(friends)
    send_message(client_socket, public_client, friend_name)
    send_message(client_socket, public_client, friend_ip)
    send_message(client_socket, public_client, friend_port)
    for key in friend_public_key:
        if key != None:
            send_key(client_socket, key)


def update_personal_status(database, userid, status):
    friends = get_friend(database, userid).fetchall()
    for friend in friends:
        if friend[1] in client_name_list:
            myidx = client_name_list.index(userid)
            fridx = client_name_list.index(friend[1])
            tmp_socket = client_socket_list[fridx]
            tmp_public_key = client_public_key[fridx]
            send_message(tmp_socket, tmp_public_key, "UPDATE_FRIEND_STATUS")
            send_message(tmp_socket, tmp_public_key, userid)
            if status == "offline":
                ip = "NULL"
                port = "NULL"
                send_message(tmp_socket, tmp_public_key, f"{ip}:{port}")
            else:
                ip, port = client_address_list[myidx]
                send_message(tmp_socket, tmp_public_key, f"{ip}:{port}")
                send_key(tmp_socket, client_public_key[myidx])



# Run server ------------------------------------
if __name__ == '__main__':
    load_data('user.sql')
    server()
