import socket
import threading
from database import *

HOST_IP = socket.gethostbyname(socket.gethostname())
HOST_PORT = 5050
ENCODER = 'utf-8'
BYTESIZE = 1024
DISCONNECT = "!DISCONNECT!"


clients = []
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST_IP, HOST_PORT))


def service():
    try:
        cmd = recv_msg()
        connected = True
        while connected:
            cmd = recv_msg()
            if cmd != None:
                print(cmd)
            if cmd == DISCONNECT:
                print(f"[SERVER]: {username} is offline!")
                update()
                connected = False
            if cmd == "Friend List":
                pass
            if cmd == "Friend Request":
                pass
            if cmd == "Add Friend":
                pass
            if cmd == "Accept Friend Request":
                pass
            if cmd == "Reject Friend Request":
                pass
            if cmd == "Friend Address":
                pass
            if cmd == "Online Users":
                online_list()
        stop()
    except:
        pass


def online_list():
    msg = "| "
    for user in online_users:
        msg += (user + " | ")
    send_msg(msg)


def friend_list():
    msg = "| "
    for friend in user_db.get(username).friend_list:
        msg += friend + " | "
    send_msg(msg)


def friend_request():
    msg = "| "
    for req in user_db.get(username).friend_request:
        msg += req + " | "
    send_msg(msg)


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

        username = username
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

    # if flag == "REGISTER":
    #     if register(list_cmd[1], list_cmd[2]):
    #         send_msg("Register successfully!")
    #         verify()
    # if flag == "FORGOTPASS":
    #     pass

def server():
    print('[SERVER]: Server is running . . . ')
    print(
        f'[SERVER]: Server is listening on port: {HOST_PORT}, ip: {HOST_IP} ')
    server_socket.listen()
    while True:
        conn, addr = server_socket.accept()
        thread = threading.Thread(target=verify, args=(conn, addr,))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count()-1}")
    server_socket.close()


if __name__ == '__main__':
    load_data()
    server()
