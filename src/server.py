import tkinter, socket, threading, os
from tkinter import *
from tkinter import messagebox
from theme import *
from tkinter.messagebox import askyesno, showerror
from tkinter import filedialog

# Defining constant
HOSTNAME = 'localhost'
PORT = socket.gethostbyname(HOSTNAME)
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
user_account_list = []

# Create a server socket using TCP protocol
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOSTNAME, PORT))
server_socket.listen()

# Connecting client
def connect_client():
    while True:
        client_socket, client_address = server_socket.accept()
        client_thread = threading.Thread(target=recieve_message, args=(client_socket, client_address,))
        client_thread.start()


def recieve_message(client_socket, client_address):
    