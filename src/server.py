import socket
import threading
from db import *
import time

HOST_IP = socket.gethostbyname('localhost')
HOST_PORT = 50000
ENCODER = 'utf-8'
BYTESIZE = 1024

clients = []
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST_IP, HOST_PORT))
server_socket.listen()


# def service(conn, addr):
#     try:
#         connected = True
#         print('Hello')
#         while connected:
#             cmd = conn.recv(BYTESIZE).decode(ENCODER)
#             if cmd != None:
#                 print(cmd)
#             if cmd == DISCONNECT:
#                 print(f"[SERVER]: {username} is offline!")
#                 connected = False
#             if cmd == "Friend List":
#                 pass
#             if cmd == "Friend Request":
#                 pass
#             if cmd == "Add Friend":
#                 pass
#             if cmd == "Accept Friend Request":
#                 pass
#             if cmd == "Reject Friend Request":
#                 pass
#             if cmd == "Friend Address":
#                 pass
#             if cmd == "Online Users":
#                 online_list()
#     except:
#         stop(conn)
#
#
# def online_list():
#     msg = "| "
#     for user in online_users:
#         msg += (user + " | ")
#
#
# def friend_list():
#     msg = "| "
#     for friend in user_db.get(username).friend_list:
#         msg += friend + " | "
#
#
# def friend_request():
#     msg = "| "
#     for req in user_db.get(username).friend_request:
#         msg += req + " | "


def add_friend():
    pass


def accept_friend_request():
    pass


def reject_friend_request():
    pass


def login(username, password):
    if user_db.get(username) == None or password != user_db.get(username).password:
        send_msg("[SERVER]: Incorrect Login Information!")
        return False
    if password == user_db.get(username).password:
        send_msg("[SERVER]: Login Successful!")
        print(f"[INFO]: {username} logged in!")

def stop(conn):
    conn.close()


def login(conn, username, password):
    if user_db.get(username) == None or password != user_db.get(username).password:
        send_msg(conn, "FAIL")
        return False
    elif password == user_db.get(username).password:
        print(f"[INFO]: {username} logged in!")
        send_msg(conn, 'SUCCESS')
        send_msg(conn, user_db.get(username).email)
        send_msg(conn, 'NULL')
        send_msg(conn, 'NULL')
        send_msg(conn, 'NULL')
        online_users.append(username)
        return True


# def register(username, password):
#     try:
#         if user_db.get(username) != None:
#             send_msg("[SERVER]: Username is already taken!")
#             return False
#         if username == None or password == None:
#             send_msg("[SERVER]: Username/Password is invalid!")
#             return False
#         add_user(username, password)
#         return True
#     except:
#         pass


def verify(conn, addr):
    # send_msg("!Verification Process!")
    # send_msg("\"Register\" command to make a new account!")
    # send_msg("\"Login\" command to login!")
    flag, message = server_socket.recv(BYTESIZE).decode(ENCODER).split(' ')
    if flag == "LOGIN":
        userid, password = message.split(':')
        if login(userid, password):
            pass

    # if flag == "REGISTER":
    #     if register(list_cmd[1], list_cmd[2]):
    #         send_msg("Register successfully!")
    #         verify()
    # if flag == "FORGOTPASS":
    #     pass
    
def register(conn, username, password):
    try:
        if user_db.get(username) != None:
            return False
        if username == None or password == None:
            return False
        add_user(username, password)
        return True
    except:
        pass


def cmd_parser(cmd):
    list_cmd = []
    temp = cmd.split(" ")
    list_cmd.append(temp[0])
    if temp[0] == "LOGIN" or temp[0] == "REGISTER":
        temp1 = temp[1].split("_")
        username = temp1[0]
        password = temp1[1]
        if len(username) == 0:
            username = None
        if len(password) == 0:
            password = None
        list_cmd.append(username)
        list_cmd.append(password)
    if temp[0] == "FORGOTPASS":
        pass
    return list_cmd

def send_msg(conn, msg):
    time.sleep(0.01)
    conn.send(msg.encode(ENCODER))


def server():
    print('[SERVER]: Server is running . . . ')
    print(
        f'[SERVER]: Server is listening on port: {HOST_PORT}, ip: {HOST_IP} ')
    while True:
        conn, addr = server_socket.accept()
        thread = threading.Thread(target=verify, args=(conn, addr,))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count()-1}")
    server_socket.close()


if __name__ == '__main__':
    load_data()
    server()
