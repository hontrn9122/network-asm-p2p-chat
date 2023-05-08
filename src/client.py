# Client Chat App
# import sys
import json
import sys
import tkinter
import socket
import threading
import os
import time
import rsa
from tkinter import *
from tkinter import messagebox
from theme import *
from tkinter.messagebox import askyesno, showerror
from tkinter import filedialog

# Defining constant
S_HOSTNAME = "localhost"
S_IP = socket.gethostbyname(S_HOSTNAME)
S_PORT = 50000
ACC_SERVER = (S_IP, S_PORT)
MY_PORT = 0
LISTEN_ADDRESS = ('localhost', MY_PORT)
ENCODER = 'utf-8'
BYTESIZE = 1024
PUB_KEY, PRI_KEY = rsa.newkeys(1024)

# Server public key
public_server = None

class login_window:
    def __init__(self):
        # define Login window
        self.login_page = tkinter.Tk()
        self.login_page.title("Simple P2P Chat application - Login")
        self.login_page.geometry("600x300")
        self.login_page.resizable(None, None)

        # set windows colors
        self.login_page.config(bg=darkgreen)

        # Define GUI Layout
        # Create Frames
        self.login_frame = tkinter.Frame(self.login_page, bg=darkgreen)

        self.login_frame.pack(pady=30)

        # Frame Layout
        self.login_label = tkinter.Label(self.login_frame, text="Login", font=(
            "haveltica", 18), fg=yellow, bg=darkgreen)
        self.uid_label = tkinter.Label(
            self.login_frame, text="User ID:", font=my_font, fg=yellow, bg=darkgreen)
        self.uid_entry = tkinter.Entry(
            self.login_frame, borderwidth=0, font=my_font)
        self.pw_label = tkinter.Label(
            self.login_frame, text="Password:", font=my_font, fg=yellow, bg=darkgreen)
        self.pw_entry = tkinter.Entry(
            self.login_frame, borderwidth=0, font=my_font, show='*')
        self.signin_button = tkinter.Button(self.login_frame, text="Sign in", font=my_font, fg=black,
                                            bg=yellow, borderwidth=0, width=10, height=3, command=lambda: self.check_fields())
        self.register_button = tkinter.Button(self.login_frame, text="Register", font=my_font_small,
                                              fg=white, bg=lightgreen, borderwidth=0, width=8, command=lambda: self.register())
        self.forgotpw_button = tkinter.Button(self.login_frame, text="Forgot password", font=my_font_small,
                                              fg=white, bg=lightgreen, borderwidth=0, width=16, command=lambda: self.forgot_password())
        self.showpasswd_button = tkinter.Checkbutton(self.login_frame, text="Show password", font=my_font_small, fg="orange",
                                                     bg=darkgreen, activebackground=darkgreen, command=lambda: self.show_passwd(self.pw_entry), anchor='w')

        self.login_label.grid(row=0, column=0, columnspan=4, padx=2, pady=10)
        self.uid_label.grid(row=1, column=0, padx=2, pady=5)
        self.uid_entry.grid(row=1, column=1, columnspan=2, padx=2, pady=5)
        self.pw_label.grid(row=2, column=0, padx=2, pady=5)
        self.pw_entry.grid(row=2, column=1, columnspan=2, padx=2, pady=5)
        self.signin_button.grid(row=1, column=3, rowspan=2, padx=10, pady=5)
        self.showpasswd_button.grid(
            row=3, column=1, columnspan=2, padx=10, pady=5)
        self.register_button.grid(row=4, column=1, padx=10, pady=5)
        self.forgotpw_button.grid(row=4, column=2, padx=10, pady=5)

        #
        self.login_page.protocol("WM_DELETE_WINDOW", self.close)


    def show_passwd(self, entry_field):
        if entry_field.cget('show') == '*':
            entry_field.config(show='')
        else:
            entry_field.config(show='*')

    def check_fields(self):
        if self.uid_entry.get() == "" or self.pw_entry == "":
            messagebox.showwarning("Missing field(s)!", "Please fill in every field(s)!")
        else:
            self.login()

    def login(self):
        # global myID, password, friend_list, server_sock, login_win, friendlist_win
        myID = self.uid_entry.get()
        password = self.pw_entry.get()
        server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            server_sock.connect(ACC_SERVER)
        except:
            messagebox.showerror(
                "Connect failed!", "Cannot connect to the server!")
            return
        global public_server
        server_sock.send(PUB_KEY.save_pkcs1("PEM"))
        public_server = rsa.PublicKey.load_pkcs1(server_sock.recv(BYTESIZE))
        server_sock.send(rsa.encrypt(f"LOGIN {myID}:{password}".encode(ENCODER), public_server))
        response = rsa.decrypt(server_sock.recv(BYTESIZE), PRI_KEY).decode(ENCODER)
        if response == "FAIL":
            messagebox.showwarning("Login failed!", "Incorrect User ID or Password!")
        else:
            email = rsa.decrypt(server_sock.recv(BYTESIZE), PRI_KEY).decode(ENCODER)
            friend_name = rsa.decrypt(server_sock.recv(BYTESIZE), PRI_KEY).decode(ENCODER).split(' ')
            friend_ip = rsa.decrypt(server_sock.recv(BYTESIZE), PRI_KEY).decode(ENCODER).split(' ')
            friend_port = rsa.decrypt(server_sock.recv(BYTESIZE), PRI_KEY).decode(ENCODER).split(' ')
            friend_list = {}
            friend_key_list = {}
            if friend_name[0] != "NULL":
                for i in range(len(friend_name)):
                    if friend_ip[i] == "NULL":
                        friend_list[friend_name[i]] = (friend_ip[i], friend_port[i])
                    else:
                        friend_list[friend_name[i]] = (friend_ip[i], int(friend_port[i]))
                        friend_key_list[friend_name[i]] = rsa.PublicKey.load_pkcs1(
                            server_sock.recv(BYTESIZE)
                        )

            # Send listen address to server
            listen_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            listen_sock.bind(LISTEN_ADDRESS)
            listen_sock.listen()
            listen_sock_address = listen_sock.getsockname()
            server_sock.send(rsa.encrypt(f"{str(listen_sock_address[0])}:{str(listen_sock_address[1])}".encode(ENCODER), public_server))
            print(f"{myID} is listening on {listen_sock_address}")
            self.close()
            frlist_window(myID, password, email, friend_list, friend_key_list, server_sock, listen_sock)

    def register(self):
        register_window()
        self.close()

    def forgot_password(self):
        forgotPassword_window()
        self.close()

    def close(self):
        self.login_page.destroy()

    def render(self):
        self.login_page.mainloop()


class frlist_window:
    def __init__(self, myID: str, password: str, email: str, friend_list: dict, friend_key_list: dict, server_sock: socket, listen_sock: socket):
        self.myID = myID
        self.password = password
        self.email = email
        self.friend_list = friend_list
        self.friend_key_list = friend_key_list
        self.server_sock = server_sock
        self.listen_sock = listen_sock
        self.conversation_list = {}
        self.friend_request = []
        self.chat_room_list = []
        self.add_fr = None
        self.fr_request = None
        self.flag = False

        # Separate friend into online and offline list
        self.onlinelist = []
        self.offlinelist = []

        # define FRIEND LIST window
        self.flist_page = tkinter.Tk()
        self.flist_page.title("Simple P2P Chat application - Friends List")
        self.flist_page.geometry("700x800")
        self.flist_page.resizable(None, None)

        # set window colors
        self.flist_page.config(bg=darkgreen)

        # Define GUI Layout
        # Create Frames
        self.info_frame = tkinter.Frame(self.flist_page, bg=yellow)
        self.label_frame = tkinter.Frame(self.flist_page, bg=darkgreen)
        self.search_frame = tkinter.Frame(self.flist_page, bg=white)
        self.list_frame = tkinter.Frame(self.flist_page, bg=white)
        self.button_frame = tkinter.Frame(self.flist_page, bg=white)

        self.info_frame.pack(pady=15)
        self.label_frame.pack(pady=0)
        self.search_frame.pack(pady=10)
        self.list_frame.pack()
        self.button_frame.pack(pady=5)

        # Info Frame Layout
        self.name_label = tkinter.Label(
            self.info_frame, text="User ID:", font=my_font, fg=darkgreen, bg=yellow, width=10, anchor="nw")
        self.name = tkinter.Label(self.info_frame, text=self.myID,
                                  font=my_font, fg=darkgreen, bg=yellow, width=44, anchor="nw")
        self.mail_label = tkinter.Label(
            self.info_frame, text="User Email:", font=my_font, fg=darkgreen, bg=yellow, width=10, anchor="nw")
        self.mail = tkinter.Label(self.info_frame, text=self.email,
                                  font=my_font, fg=darkgreen, bg=yellow, width=44, anchor="nw")

        self.name_label.grid(row=0, column=0, padx=5, pady=5)
        self.name.grid(row=0, column=1, columnspan=2, padx=5, pady=5)
        self.mail_label.grid(row=1, column=0, padx=5, pady=5)
        self.mail.grid(row=1, column=1, columnspan=2, padx=5, pady=5)

        # Label Frame Layout
        self.friend_list_label = tkinter.Label(self.label_frame, text="Friend List", font=(
            'haveltica', 18), fg=white, bg=darkgreen, width=23, anchor="nw")
        self.frrequest_button = tkinter.Button(self.label_frame, text="Friend request", borderwidth=0,
                                               width=10, font=my_font_small, bg=yellow, fg=black, command=lambda: self.show_friend_request())
        self.addfr_button = tkinter.Button(self.label_frame, text="Add friend", borderwidth=0,
                                           width=10, font=my_font_small, bg=yellow, fg=black, command=lambda: self.add_friend())
        self.chatroom_button = tkinter.Button(self.label_frame, text="Chat room", borderwidth=0,
                                           width=10, font=my_font_small, bg=yellow, fg=black,
                                           command=lambda: self.chat_room())
        self.friend_list_label.grid(row=0, column=0, padx=5, pady=5)
        self.chatroom_button.grid(row=0, column=1, padx=5, pady=5)
        self.frrequest_button.grid(row=0, column=2, padx=5, pady=5)
        self.addfr_button.grid(row=0, column=3, padx=5, pady=5)

        # List Frame Layout
        self.my_scrollbar = tkinter.Scrollbar(self.list_frame, orient=VERTICAL)
        self.my_listbox = tkinter.Listbox(self.list_frame, height=20, width=55, borderwidth=0, bg=white,
                                          fg=darkgreen, font=my_font, yscrollcommand=self.my_scrollbar.set, selectmode=SINGLE)
        self.my_scrollbar.config(command=self.my_listbox.yview)
        self.my_listbox.grid(row=0, column=0)
        self.my_scrollbar.grid(row=0, column=1, sticky="NS")

        # Search Frame Layout
        self.input_entry = tkinter.Entry(
            self.search_frame, width=44, borderwidth=0, font=my_font)
        self.search_button = tkinter.Button(
            self.search_frame, text="Search", borderwidth=0, width=10, font=my_font, bg=yellow, fg=black)
        self.input_entry.grid(row=0, column=0, padx=5, pady=5)
        self.search_button.grid(row=0, column=1, padx=5, pady=5)
        self.input_entry.bind("<KeyRelease>", self.search_check)
        self.search_button.bind("<Button-1>", self.search_check)

        # Button Frame Layout
        self.unfriend_button = tkinter.Button(self.button_frame, text="Unfriend", width=27,
                                              borderwidth=0, font=my_font, bg=yellow, fg=black, command=lambda: self.unfriend())
        self.chat_button = tkinter.Button(self.button_frame, text="Start chatting", width=27,
                                          borderwidth=0, font=my_font, bg=yellow, fg=black, command=lambda: self.start_conversation())
        self.unfriend_button.grid(row=0, column=0, padx=5, pady=5)
        self.chat_button.grid(row=0, column=1, padx=5, pady=5)

        # Create display list
        self.update_friend_status()
        self.update_displaylist(self.onlinelist, self.offlinelist)

        # Pop up confirm message when quit
        self.flist_page.protocol("WM_DELETE_WINDOW", self.close_confirm)

        # Create a thread for listening incoming update from server
        self.update_thread = threading.Thread(target=self.listen_server, daemon=True)
        self.update_thread.start()

        # Create a thread for listening to friend connections
        self.connections_thread = threading.Thread(target=self.listen_to_friend, daemon=True)
        self.connections_thread.start()

        self.flist_page.mainloop()

    def search_check(self, event):
        typed = self.input_entry.get()
        if typed == '':
            self.update_displaylist(self.onlinelist, self.offlinelist)
        else:
            online_tmplist = []
            offline_tmplist = []
            for user in self.onlinelist:
                if typed.lower() in user.lower():
                    online_tmplist.append(user)
            for user in self.offlinelist:
                if typed.lower() in user.lower():
                    offline_tmplist.append(user)
            self.update_displaylist(online_tmplist, offline_tmplist)

    def update_friend_status(self):
        self.onlinelist.clear()
        self.offlinelist.clear()
        for userid in self.friend_list:
            if self.friend_list[userid] == ('NULL', 'NULL'):
                self.offlinelist.append(userid)
            else:
                self.onlinelist.append(userid)

    def update_displaylist(self, onlinelist, offlinelist):
        self.my_listbox.delete(0, END)
        for user in offlinelist:
            self.my_listbox.insert(END, user)
            self.my_listbox.itemconfig(END, {'fg': 'gray63'})
        for user in onlinelist:
            self.my_listbox.insert(0, user)
            self.my_listbox.itemconfig(0, {'fg': 'green2'})

    def start_conversation(self):
        chosen = self.my_listbox.curselection()
        if len(chosen) == 0:
            showerror(title="No friend selected!",
                      message=f"Please choose a friend to start chatting!")
        else:
            friend_ID = self.my_listbox.get(chosen[0])
            self.connect_to_friend(friend_ID)

    def listen_server(self):
        while True:
            # try:
                server_mess = rsa.decrypt(self.server_sock.recv(BYTESIZE), PRI_KEY).decode(ENCODER)
                if server_mess == "FRIEND_LIST_UPDATE":
                    self.frlist_update()
                    self.update_displaylist(self.onlinelist, self.offlinelist)
                elif server_mess == "UPDATE_FRIEND_STATUS":
                    friend_name = rsa.decrypt(self.server_sock.recv(BYTESIZE), PRI_KEY).decode(ENCODER)
                    friend_address = rsa.decrypt(self.server_sock.recv(BYTESIZE), PRI_KEY).decode(ENCODER).split(':')
                    if friend_address[0] == "NULL":
                        self.friend_list[friend_name] = (friend_address[0], friend_address[1])
                    else:
                        self.friend_list[friend_name] = (friend_address[0], int(friend_address[1]))
                        self.friend_key_list[friend_name] = rsa.PublicKey.load_pkcs1(
                            self.server_sock.recv(BYTESIZE)
                        )
                    self.update_friend_status()
                    self.update_displaylist(self.onlinelist, self.offlinelist)
                elif server_mess == "FRIEND_REQUEST":
                    user_ID = rsa.decrypt(self.server_sock.recv(BYTESIZE), PRI_KEY).decode(ENCODER)
                    if user_ID not in self.friend_request:
                        self.friend_request.append(user_ID)
                elif server_mess == "REQUEST_TIMEOUT":
                    user_ID = rsa.decrypt(self.server_sock.recv(BYTESIZE), PRI_KEY).decode(ENCODER)
                    messagebox.showinfo(
                        "Friend request timeout!", f"Friend request to {user_ID} has timed out!")
                elif server_mess == "REQUEST_DENIED":
                    user_ID = rsa.decrypt(self.server_sock.recv(BYTESIZE), PRI_KEY).decode(ENCODER)
                    messagebox.showinfo(
                        "Friend request denied!", f"Friend request to {user_ID} has been denied!")
                elif server_mess == "DEL_TIMEOUT_REQUEST":
                    user_ID = rsa.decrypt(self.server_sock.recv(BYTESIZE), PRI_KEY).decode(ENCODER)
                    if user_ID in self.friend_request:
                        self.friend_request.remove(user_ID)
                elif server_mess == "FOUND_ONLINE":
                    self.add_fr.set_message(server_mess)
                elif server_mess == "FOUND_OFFLINE":
                    self.add_fr.set_message(server_mess)
                elif server_mess == "NOTFOUND":
                    self.add_fr.set_message(server_mess)
            # except:
            #     if self.flag:
            #         sys.exit()
            #     showerror(title="Server connection lost!", message=f"Cannot connect to server!")
            #     self.server_sock.close()
            #     break

    def frlist_update(self):
        # global friend_list, server_sock
        friend_name = rsa.decrypt(self.server_sock.recv(BYTESIZE), PRI_KEY).decode(ENCODER).split(' ')
        friend_ip = rsa.decrypt(self.server_sock.recv(BYTESIZE), PRI_KEY).decode(ENCODER).split(' ')
        friend_port = rsa.decrypt(self.server_sock.recv(BYTESIZE), PRI_KEY).decode(ENCODER).split(' ')

        if friend_name[0] != "NULL":
            for i in range(len(friend_name)):
                if friend_ip[i] == "NULL":
                    self.friend_list[friend_name[i]] = (friend_ip[i], friend_port[i])
                else:
                    self.friend_list[friend_name[i]] = (friend_ip[i], int(friend_port[i]))
                    self.friend_key_list[friend_name[i]] = rsa.PublicKey.load_pkcs1(
                        self.server_sock.recv(BYTESIZE)
                    )
        self.update_friend_status()

    def listen_to_friend(self):
        # Verify and Accept or Deny Connection
        while not self.flag:
            connected_client, address = self.listen_sock.accept()
            connected_id = rsa.decrypt(connected_client.recv(BYTESIZE), PRI_KEY).decode(ENCODER)
            if connected_id in self.friend_list:
                # print("Connected with {}".format(str(address)))
                self.conversation_list[connected_id] = conversation_window(
                    self.flist_page, self.myID, self.email,
                    self.friend_key_list[connected_id], connected_id, connected_client)
            else:
                connected_client.close()

    def connect_to_friend(self, friend_ID):
        print(self.friend_list[friend_ID])
        # global sock_list
        if friend_ID not in self.conversation_list or not self.conversation_list[friend_ID].active:
            new_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            friend_ip, friend_port = self.friend_list[friend_ID]
            new_socket.connect((friend_ip, friend_port))
            friend_key = self.friend_key_list[friend_ID]
            new_socket.send(rsa.encrypt(self.myID.encode(ENCODER), friend_key))
            self.conversation_list[friend_ID] = conversation_window(
                self.flist_page, self.myID, self.email, friend_key, friend_ID, new_socket)
        else:
            self.conversation_list[friend_ID].bring_to_front()

    # def check_address(self, address):
    #     for userid in self.friend_list:
    #         if self.friend_list[userid] == address:
    #             return userid
    #     return "NULL"

    def add_friend(self):
        if self.add_fr is None or not self.add_fr.active:
            self.add_fr = addFriend_window(self.flist_page, self.server_sock, "")
        else:
            self.add_fr.bring_to_front()

    def unfriend(self):
        chosen = self.my_listbox.curselection()
        if len(chosen) == 0:
            showerror(title="No friend selected!", message=f"Please choose a friend to remove!")
        else:
            friend_ID = self.my_listbox.get(chosen[0])
            self.server_sock.send(rsa.encrypt(f"UNFRIEND {friend_ID}".encode(ENCODER), public_server))
            self.friend_list.pop(friend_ID)
            if friend_ID in self.offlinelist:
                self.offlinelist.remove(friend_ID)
            if friend_ID in self.onlinelist:
                self.onlinelist.remove(friend_ID)
            self.update_displaylist(self.onlinelist, self.offlinelist)

    def show_friend_request(self):
        if self.fr_request is None or not self.fr_request.active:
            self.fr_request = friendRequest_window(self.flist_page, self.server_sock, self.friend_request)
        else:
            self.fr_request.bring_to_front()

    def chat_room(self):
        pass

    def create_chatroom(self):
        pass

    def close_confirm(self):
        confirm_reply = askyesno(
            title="Log out?", message="You will log out this user once you close this window!\nDo you want to log out?")
        if confirm_reply:
            self.flag = True
            self.server_sock.send(rsa.encrypt(f"FRIEND_REQUEST_TIMEOUT {json.dumps(self.friend_request)}".encode(ENCODER), public_server))
            for friend in self.conversation_list:
                if self.conversation_list[friend].active:
                    self.conversation_list[friend].disconnect()
                self.conversation_list.pop(friend)
            self.server_sock.close()
            self.flist_page.destroy()
            test = login_window()
            test.render()



class conversation_window:
    def __init__(self, root: Tk, myID: str, email: str, friend_key, userid: str, user_socket: socket):
        self.active = True
        self.userid = userid
        self.user_socket = user_socket
        self.friend_key = friend_key
        # define CONVERSATION window
        self.conver_page = tkinter.Toplevel(root)
        self.conver_page.title(
            f"Simple P2P Chat application - Conversation with {self.userid}")
        self.conver_page.geometry("700x700")
        self.conver_page.resizable(None, None)

        # set window colors
        self.conver_page.config(bg=darkgreen)

        # Define GUI Layout
        # Create Frames
        self.info_frame = tkinter.Frame(self.conver_page, bg=yellow)
        self.label_frame = tkinter.Frame(self.conver_page, bg=darkgreen)
        self.input_frame = tkinter.Frame(self.conver_page, bg=white)
        self.output_frame = tkinter.Frame(self.conver_page, bg=white)

        self.info_frame.pack(pady=10)
        self.label_frame .pack(pady=10)
        self.output_frame.pack(pady=10)
        self.input_frame.pack()

        # Info Frame Layout
        self.name_label = tkinter.Label(
            self.info_frame, text="User ID:", font=my_font, fg=darkgreen, bg=yellow, width=10, anchor="nw")
        self.name = tkinter.Label(
            self.info_frame, text=myID, font=my_font, fg=darkgreen, bg=yellow, width=44, anchor="nw")
        self.mail_label = tkinter.Label(
            self.info_frame, text="User Email:", font=my_font, fg=darkgreen, bg=yellow, width=10, anchor="nw")
        self.mail = tkinter.Label(
            self.info_frame, text=email, font=my_font, fg=darkgreen, bg=yellow, width=44, anchor="nw")

        self.name_label.grid(row=0, column=0, padx=5, pady=5)
        self.name.grid(row=0, column=1, columnspan=2, padx=5, pady=5)
        self.mail_label.grid(row=1, column=0, padx=5, pady=5)
        self.mail.grid(row=1, column=1, columnspan=2, padx=5, pady=5)

        self.friend_list_label = tkinter.Label(self.label_frame, text=f"Chatting with {self.userid}", font=(
            'haveltica', 18), fg=white, bg=darkgreen, width=44, anchor="nw")
        self.friend_list_label.grid(row=0, column=0, padx=5, pady=5)

        # Output Frame Layout
        self.my_scrollbar = tkinter.Scrollbar(self.output_frame, orient=VERTICAL)
        self.my_listbox = tkinter.Listbox(self.output_frame, height=20, width=55, borderwidth=0,
                                          bg=white, fg=darkgreen, font=my_font, yscrollcommand=self.my_scrollbar.set)
        self.my_scrollbar.config(command=self.my_listbox.yview)
        self.my_listbox.grid(row=0, column=0)
        self.my_scrollbar.grid(row=0, column=1, sticky="NS")

        # Input Frame Layout
        self.input_entry = tkinter.Entry(
            self.input_frame, width=39, borderwidth=0, font=my_font)
        self.file_button = tkinter.Button(self.input_frame, text="File", borderwidth=0,
                                          width=7, font=my_font, bg=yellow, fg=black, command=lambda: self.send_file())
        self.send_button = tkinter.Button(self.input_frame, text="Send", borderwidth=0,
                                          width=7, font=my_font, bg=yellow, fg=black, command=lambda: self.send_message())
        self.input_entry.grid(row=0, column=0, padx=5, pady=5)
        self.file_button.grid(row=0, column=1, padx=5, pady=5)
        self.send_button.grid(row=0, column=2, padx=5, pady=5)

        # Pop up confirm message when quit
        self.conver_page.protocol("WM_DELETE_WINDOW", self.close_confirm)

        # Create a thread for listening incoming messages
        self.receive_thread = threading.Thread(target=self.receive_message, daemon=True)
        self.receive_thread.start()

    def add_to_list(self, message, color):
        self.my_listbox.insert(END, message)
        self.my_listbox.itemconfig(END, {'fg': color})

    def disconnect(self):
        self.user_socket.close()
        self.conver_page.destroy()

    def send_message(self):
        message = self.input_entry.get()
        print(message)
        # check_mess = []
        # for index in range(6):
        #     check_mess.append(message[index])
        # if check_mess == "<FILE>":
        #     showerror(title="Message syntax error!",
        #               message="Please do not start a message with FILE: '!")
        # else:
        # self.user_socket.send(rsa.encrypt(f"m {message}".encode(ENCODER), self.friend_key))
        send_message = f"m {message}"
        if len(send_message) > 100:
            split_mess = [send_message[i:i + 100] for i in range(0, len(send_message), 100)]
        else:
            split_mess = [send_message]
        for mess_pack in split_mess:
            self.user_socket.send(rsa.encrypt(mess_pack.encode(ENCODER), self.friend_key))
            time.sleep(0.01)
        self.user_socket.send(rsa.encrypt(b"<END_MESS>", self.friend_key))
        self.add_to_list(f"You: {message}", "gray63")
        self.input_entry.delete(0, END)

    def send_file(self):
        file_path = self.get_file()
        file_name = os.path.basename(file_path)
        file = open(file_path, 'rb')
        file_size = os.path.getsize(file_path)
        message = f"f {file_name}:{str(file_size)}"
        if len(message) > 100:
            split_mess = [message[i:i + 100] for i in range(0, len(message), 100)]
        else:
            split_mess = [message]
        for mess_pack in split_mess:
            self.user_socket.send(rsa.encrypt(mess_pack.encode(ENCODER), self.friend_key))
            time.sleep(0.01)
        self.user_socket.send(rsa.encrypt(b"<END_MESS>", self.friend_key))
        # self.user_socket.send(
        #     rsa.encrypt(f"f {file_name}:{str(file_size)}".encode(ENCODER), self.friend_key)
        # )
        time.sleep(0.01)
        data = file.read()
        self.user_socket.sendall(data)
        self.user_socket.send(b"<END_FILE>")
        self.add_to_list(f"<FILE>You: {file_name}", "blue")
        # self.my_listbox.itemconfig(END,{'font: my_font_italic_underscore'})
        file.close()

    def receive_message(self):
        while True:
            #try:
                mess_bytes = b""
                done = False
                while not done:
                    mess_data = rsa.decrypt(self.user_socket.recv(BYTESIZE), PRI_KEY)
                    mess_bytes += mess_data
                    if mess_bytes[-10:] == b"<END_MESS>":
                        done = True
                        mess_bytes = mess_bytes[:-10]
                type_mess, message = mess_bytes.decode(ENCODER).split(' ', 1)
                # type_mess, message = rsa.decrypt(self.user_socket.recv(
                #     BYTESIZE), PRI_KEY).decode(ENCODER).split(' ', 1)
                if type_mess == 'm':
                    message = '{}: {}'.format(self.userid, message)
                    self.add_to_list(message, "green3")
                else:
                    file_name = message.split(':')
                    if not os.path.exists(f"{self.userid}"):
                        os.mkdir(f"{self.userid}")
                    file_path = f"{self.userid}/{file_name[0]}"
                    is_existed = os.path.isfile(file_path)
                    i = 1
                    while is_existed:
                        file_path = f"{self.userid}/{file_name}_({str(i)})"
                        is_existed = os.path.isfile(file_path)
                        i += 1

                    file = open(file_path, 'wb')
                    file_bytes = b""
                    done = False

                    while not done:
                        file_data = self.user_socket.recv(BYTESIZE)
                        file_bytes += file_data
                        if file_bytes[-10:] == b"<END_FILE>":
                            done = True
                            file_bytes = file_bytes[:-10]

                    file.write(file_bytes)
                    file.close()
                    message = '<FILE>{}: {}'.format(self.userid, file_name[0])
                    self.add_to_list(message, "blue")
            # except:
            #     # An error occured, disconnect from the server
            #     # conver_win_list.pop(self.userid)
            #     # sock_list.pop(self.userid)
            #     showerror(title="Connection lost!",
            #               message=f"{self.userid} has left the conversation!")
            #     self.active = False
            #     self.user_socket.close()
            #     break

    def close_confirm(self):
        confirm_reply = askyesno(
            title="Leave conversation?", message="You will disconnect with this user and the conversation will be deleted when you close this window!\nDo you want to leave?")
        if confirm_reply:
            self.active = False
            self.user_socket.close()
            self.conver_page.destroy()

    def get_file(self):
        filename = filedialog.askopenfilename(title='Select a file')
        # tkinter.Label(tkinter.Toplevel(), text = self.filename).pack()
        return filename

    def bring_to_front(self):
        self.conver_page.lift()


class addFriend_window:
    def __init__(self, root: Tk, server_sock: socket, message: str):
        self.server_sock = server_sock
        self.message = message
        self.active = True

        # define ADD FRIEND window
        self.addfriend_popup = tkinter.Toplevel(root)
        self.addfriend_popup.title("Add new friend")
        self.addfriend_popup.geometry("300x160")
        self.addfriend_popup.resizable(None, None)

        # set window colors
        self.addfriend_popup.config(bg=darkgreen)

        # Define GUI Layout
        # Create Frames
        self.input_frame = tkinter.Frame(self.addfriend_popup, bg=white)
        self.output_frame = tkinter.Frame(self.addfriend_popup, bg=darkgreen)

        self.input_frame.pack(pady=15)
        self.output_frame.pack()

        # Output Frame Layout
        self.result = tkinter.Label(
            self.output_frame, text="<result>", font=my_font, fg=white, bg=darkgreen, width=20)
        self.add_button = tkinter.Button(self.output_frame, text="Send friend request", borderwidth=0, width=15,
                                         font=my_font_small, bg=yellow, fg=black, state=DISABLED, command=lambda: self.request_friend())
        self.result.grid(row=0, column=0, padx=5, pady=5)
        self.add_button.grid(row=1, column=0, padx=5, pady=5)

        # Input Frame Layout
        self.input_entry = tkinter.Entry(
            self.input_frame, width=15, borderwidth=0, font=my_font)
        self.search_button = tkinter.Button(self.input_frame, text="Search", borderwidth=0,
                                            width=5, font=my_font, bg=yellow, fg=black, command=lambda: self.check_fields())
        self.input_entry.grid(row=0, column=0, padx=5, pady=5)
        self.search_button.grid(row=0, column=1, padx=5, pady=5)

        self.addfriend_popup.protocol("WM_DELETE_WINDOW", self.close_confirm)

    def close_confirm(self):
        self.active = False
        self.addfriend_popup.destroy()

    def bring_to_front(self):
        self.addfriend_popup.lift()

    def check_fields(self):
        if self.input_entry.get() == "":
            messagebox.showwarning("Missing field(s)!", "Please enter an UserId!")
        else:
            self.find_user()

    def set_message(self, message):
        self.message = message

    def find_user(self):
        user_id = self.input_entry.get()
        self.server_sock.send(rsa.encrypt(f"FIND {user_id}".encode(ENCODER), public_server))
        time.sleep(0.01)
        if self.message == "FOUND_ONLINE":
            self.result.config(text=f"{user_id} is online")
            self.add_button.config(state=NORMAL)
        elif self.message == "FOUND_OFFLINE":
            self.result.config(text=f"{user_id} is offline")
        elif self.message == "NOTFOUND":
            self.result.config(text="Not found!")

    def request_friend(self):
        self.add_button.config(state=DISABLED)
        user_id = self.input_entry.get()
        self.server_sock.send(rsa.encrypt(f"REQUEST {user_id}".encode(ENCODER), public_server))
        self.set_message("")
        self.result.config(text="<result>")
        self.add_button.config(state=DISABLED)


class register_window:
    def __init__(self):
        #define REGISTER window
        self.register_page = tkinter.Tk()
        self.register_page.title("Register Account")
        self.register_page.geometry("300x450")
        self.register_page.resizable(None, None)

        #set window colors
        self.register_page.config(bg=darkgreen)

        #Define GUI Layout
        #Create Frames
        self.register_frame = tkinter.Frame(self.register_page, bg=darkgreen)
        self.register_frame.pack(pady=15)

        #Input Frame Layout
        self.register_label = tkinter.Label(self.register_frame, text="Register", font=("haveltica", 18), fg=yellow, bg=darkgreen)
        self.uid_label = tkinter.Label(self.register_frame, text="User ID:", font=my_font, fg=yellow, bg=darkgreen)
        self.uid_entry = tkinter.Entry(self.register_frame, borderwidth=0, font=my_font)
        self.email_label = tkinter.Label(self.register_frame, text="Email:", font=my_font, fg=yellow, bg=darkgreen)
        self.email_entry = tkinter.Entry(self.register_frame, borderwidth=0, font=my_font)
        self.pw_label = tkinter.Label(self.register_frame, text="Password:", font=my_font, fg=yellow, bg=darkgreen)
        self.pw_entry = tkinter.Entry(self.register_frame, borderwidth=0, font=my_font, show='*')
        self.confirmpw_label = tkinter.Label(self.register_frame, text="Confirm Password:", font=my_font, fg=yellow, bg=darkgreen)
        self.confirmpw_entry = tkinter.Entry(self.register_frame, borderwidth=0, font=my_font, show='*')
        self.register_button = tkinter.Button(self.register_frame, text="Sign Up", font=my_font, fg = white, bg=lightgreen, borderwidth=0, width=8, command=lambda: self.check_fields())

        self.register_label.grid(row=0, column=0, padx=2, pady=10)
        self.uid_label.grid(row=1, column=0, pady=5, sticky='W')
        self.uid_entry.grid(row=2, column=0, padx=2, pady=5)
        self.email_label.grid(row=3, column=0, pady=5, sticky='W')
        self.email_entry.grid(row=4, column=0, padx=2, pady=5)
        self.pw_label.grid(row=5, column=0, pady=5, sticky='W')
        self.pw_entry.grid(row=6, column=0, padx=2, pady=5)
        self.confirmpw_label.grid(row=7, column=0, pady=5, sticky='W')
        self.confirmpw_entry.grid(row=8, column=0, padx=2, pady=5)
        self.register_button.grid(row=9, column=0, padx=2, pady=15)

        #Pop up confirm message when quit
        self.register_page.protocol("WM_DELETE_WINDOW", self.close_confirm)

    def check_fields(self):
        if self.uid_entry.get() == "" or self.pw_entry == "":
            messagebox.showwarning("Missing field(s)!", "Please fill in every field(s)!")
        else:
            self.register()

    def register(self):
        userId = self.uid_entry.get()
        email = self.email_entry.get()
        password = self.pw_entry.get()
        c_password = self.confirmpw_entry.get()
        if password != c_password:
            messagebox.showwarning("Warning!", "The confirm password is not the same!")
            return
        server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            server_sock.connect(ACC_SERVER)
        except:
            messagebox.showerror("Register failed!", "Cannot connect to the server!")
            return
        global public_server
        server_sock.send(PUB_KEY.save_pkcs1("PEM"))
        public_server = rsa.PublicKey.load_pkcs1(server_sock.recv(BYTESIZE))

        server_sock.send(rsa.encrypt(f"REGISTER {userId}:{email}:{password}".encode(ENCODER), public_server))
        response = rsa.decrypt(server_sock.recv(BYTESIZE), PRI_KEY).decode(ENCODER)
        if response == 'FAIL_USERID':
            messagebox.showerror("Register failed!", "User ID already exists!")
        elif response == 'FAIL_EMAIL':
            messagebox.showerror("Register failed!", "Email already exists!")
        else:
            listen_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            listen_sock.bind(LISTEN_ADDRESS)
            listen_sock.listen()
            listen_sock_address = listen_sock.getsockname()
            server_sock.send(
                rsa.encrypt(
                    f"{str(listen_sock_address[0])}:{str(listen_sock_address[1])}".encode(ENCODER), public_server
                )
            )

            self.register_page.destroy()
            frlist_window(userId, password, email, {}, {}, server_sock, listen_sock)


    def close_confirm(self):
        confirm_reply = askyesno(title="Cancel register?", message="Do you want cancel your register?")
        if confirm_reply:
            login_window()
            self.register_page.destroy()


class forgotPassword_window:
    def __init__(self):
        #define FORGOT PASSWORD window
        self.forgotpw_page = tkinter.Tk()
        self.forgotpw_page.title("Forgot Password")
        self.forgotpw_page.geometry("300x450")
        self.forgotpw_page.resizable(None, None)

        # set window colors
        self.forgotpw_page.config(bg=darkgreen)

        # Define GUI Layout
        # Create Frames
        self.forgotpw_frame = tkinter.Frame(self.forgotpw_page, bg=darkgreen)
        self.forgotpw_frame.pack(pady=15)

        # Input Frame Layout
        self.forgotpw_label = tkinter.Label(self.forgotpw_frame, text="Forgot Password", font=("haveltica", 18), fg=yellow, bg=darkgreen)
        self.uid_label = tkinter.Label(self.forgotpw_frame, text="User ID:", font=my_font, fg=yellow, bg=darkgreen)
        self.uid_entry = tkinter.Entry(self.forgotpw_frame, borderwidth=0, font=my_font)
        self.email_label = tkinter.Label(self.forgotpw_frame, text="Email:", font=my_font, fg=yellow, bg=darkgreen)
        self.email_entry = tkinter.Entry(self.forgotpw_frame, borderwidth=0, font=my_font)
        self.pw_label = tkinter.Label(self.forgotpw_frame, text="New Password:", font=my_font, fg=yellow, bg=darkgreen)
        self.pw_entry = tkinter.Entry(self.forgotpw_frame, borderwidth=0, font=my_font, show='*')
        self.confirmpw_label = tkinter.Label(self.forgotpw_frame, text="Confirm Password:", font=my_font, fg=yellow, bg=darkgreen)
        self.confirmpw_entry = tkinter.Entry(self.forgotpw_frame, borderwidth=0, font=my_font, show='*')
        self.confirm_button = tkinter.Button(self.forgotpw_frame, text="Confirm", font=my_font, fg=white, bg=lightgreen, borderwidth=0, width=8, command=lambda: self.check_fields())

        self.forgotpw_label.grid(row=0, column=0, padx=2, pady=10)
        self.uid_label.grid(row=1, column=0, pady=5, sticky='W')
        self.uid_entry.grid(row=2, column=0, padx=2, pady=5)
        self.email_label.grid(row=3, column=0, pady=5, sticky='W')
        self.email_entry.grid(row=4, column=0, padx=2, pady=5)
        self.pw_label.grid(row=5, column=0, pady=5, sticky='W')
        self.pw_entry.grid(row=6, column=0, padx=2, pady=5)
        self.confirmpw_label.grid(row=7, column=0, pady=5, sticky='W')
        self.confirmpw_entry.grid(row=8, column=0, padx=2, pady=5)
        self.confirm_button.grid(row=9, column=0, padx=2, pady=15)

        # Pop up confirm message when quit
        self.forgotpw_page.protocol("WM_DELETE_WINDOW", self.close_confirm)

    def check_fields(self):
        if self.uid_entry.get() == "" or self.pw_entry == "":
            messagebox.showwarning("Missing field(s)!", "Please fill in every field(s)!")
        else:
            self.forgotPassword()


    def forgotPassword(self):
        userId = self.uid_entry.get()
        email = self.email_entry.get()
        password = self.pw_entry.get()
        c_password = self.confirmpw_entry.get()
        if password != c_password:
            messagebox.showwarning("Warning!", "The confirm password is not the same!")
            return
        server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            server_sock.connect(ACC_SERVER)
        except:
            messagebox.showerror("Error!", "Cannot connect to the server!")
            return
        global public_server
        server_sock.send(PUB_KEY.save_pkcs1("PEM"))
        public_server = rsa.PublicKey.load_pkcs1(server_sock.recv(BYTESIZE))
        server_sock.send(rsa.encrypt(f"FORGOTPASS {userId}:{email}:{password}".encode(ENCODER), public_server))
        response = rsa.decrypt(server_sock.recv(BYTESIZE), PRI_KEY).decode(ENCODER)
        if response == 'FAIL':
            messagebox.showerror("Error!", "User ID or Email is uncorrected!")
        else:
            friend_name = rsa.decrypt(server_sock.recv(BYTESIZE), PRI_KEY).decode(ENCODER).split(' ')
            friend_ip = rsa.decrypt(server_sock.recv(BYTESIZE), PRI_KEY).decode(ENCODER).split(' ')
            friend_port = rsa.decrypt(server_sock.recv(BYTESIZE), PRI_KEY).decode(ENCODER).split(' ')
            friend_list = {}
            friend_key_list = {}

            if friend_name[0] != "NULL":
                for i in range(len(friend_name)):
                    if friend_ip[i] == "NULL":
                        friend_list[friend_name[i]] = (friend_ip[i], friend_port[i])
                    else:
                        friend_list[friend_name[i]] = (friend_ip[i], int(friend_port[i]))
                        friend_key_list[friend_name[i]] = rsa.PublicKey.load_pkcs1(
                            server_sock.recv(BYTESIZE)
                        )

            # Send listen address to server
            listen_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            listen_sock.bind(LISTEN_ADDRESS)
            listen_sock.listen()
            listen_sock_address = listen_sock.getsockname()
            server_sock.send(rsa.encrypt(f"{str(listen_sock_address[0])}:{str(listen_sock_address[1])}".encode(ENCODER), public_server))

            self.forgotpw_page.destroy()
            frlist_window(userId, password, email, friend_list, friend_key_list, server_sock, listen_sock)

    def close_confirm(self):
        confirm_reply = askyesno(title="Cancel?", message="Do you want to cancel?")
        if confirm_reply:
            login_window()
            self.forgotpw_page.destroy()


class friendRequest_window:
    def __init__(self, root: Tk, server_sock: socket, friend_request: list):
        self.friendrequest_list = friend_request
        self.server_sock = server_sock
        self.active = True

        # define FRIEND LIST window
        self.friendrequest_popup = tkinter.Toplevel(root)
        self.friendrequest_popup.title("Friend Request")
        self.friendrequest_popup.geometry("300x350")
        self.friendrequest_popup.resizable(None, None)

        # set window colors
        self.friendrequest_popup.config(bg=darkgreen)

        # Define GUI Layout
        # Create Frames
        self.label_frame = tkinter.Frame(self.friendrequest_popup, bg=darkgreen)
        self.list_frame = tkinter.Frame(self.friendrequest_popup, bg=darkgreen)
        self.button_frame = tkinter.Frame(self.friendrequest_popup, bg=darkgreen)

        self.label_frame.pack(pady=5)
        self.list_frame.pack()
        self.button_frame.pack(pady=5)

        # Label Frame Layout
        self.label_test = tkinter.Label(self.label_frame, text="Friend Request", font=('haveltica', 18), fg=yellow,
                                        bg=darkgreen, width=20)
        self.label_test.grid(row=0, column=0, padx=5, pady=5)

        # List Frame Layout
        self.my_scrollbar = tkinter.Scrollbar(self.list_frame, orient=VERTICAL)
        self.my_listbox = tkinter.Listbox(self.list_frame, height=10, width=25, borderwidth=0, bg=white, fg=darkgreen,
                                          font=my_font, yscrollcommand=self.my_scrollbar.set)
        self.my_scrollbar.config(command=self.my_listbox.yview)
        self.my_listbox.grid(row=0, column=0)
        self.my_scrollbar.grid(row=0, column=1, sticky="NS")

        # Button Frame Layout
        self.accept_button = tkinter.Button(self.button_frame, text="Accept", width=10, borderwidth=0, font=my_font,
                                            bg=yellow, fg=black, command=lambda: self.accept())
        self.refuse_button = tkinter.Button(self.button_frame, text="Refuse", width=10, borderwidth=0, font=my_font,
                                            bg=yellow, fg=black, command=lambda: self.refuse())
        self.accept_button.grid(row=0, column=0, padx=5, pady=5)
        self.refuse_button.grid(row=0, column=1, padx=5, pady=5)

        self.update_displaylist()
        self.friendrequest_popup.protocol("WM_DELETE_WINDOW", self.close_confirm)

    def close_confirm(self):
        self.active = False
        self.friendrequest_popup.destroy()

    def bring_to_front(self):
        self.friendrequest_popup.lift()

    def update_friendlist(self, fr_list):
        self.friendrequest_list = fr_list
        self.update_displaylist()

    def update_displaylist(self):
        self.my_listbox.delete(0, END)
        for user in self.friendrequest_list:
            self.my_listbox.insert(0, user)
            self.my_listbox.itemconfig(0, {'fg': 'green2'})

    def accept(self):
        chosen = self.my_listbox.curselection()
        if len(chosen) == 0:
            showerror(title="No friend selected!",
                      message=f"Please choose a friend !")
        else:
            userid = self.my_listbox.get(chosen[0])
            self.server_sock.send(rsa.encrypt(f"ACCEPT_FRIEND {userid}".encode(ENCODER), public_server))
            self.friendrequest_list.remove(userid)
            self.update_displaylist()

    def refuse(self):
        chosen = self.my_listbox.curselection()
        if len(chosen) == 0:
            showerror(title="No friend selected!",
                      message=f"Please choose a friend!")
        else:
            userid = self.my_listbox.get(chosen[0])
            self.server_sock.send(rsa.encrypt(f"REFUSE_FRIEND {userid}".encode(ENCODER), public_server))
            self.friendrequest_list.remove(userid)
            self.update_displaylist()


class chatroom_window:
    def __init__(self, root: Tk, server_sock: socket, friend_request: list):
        self.friendrequest_list = friend_request
        self.server_sock = server_sock
        self.active = True

        # define FRIEND LIST window
        self.friendrequest_popup = tkinter.Toplevel(root)
        self.friendrequest_popup.title("Friend Request")
        self.friendrequest_popup.geometry("300x350")
        self.friendrequest_popup.resizable(None, None)

        # set window colors
        self.friendrequest_popup.config(bg=darkgreen)

        # Define GUI Layout
        # Create Frames
        self.label_frame = tkinter.Frame(self.friendrequest_popup, bg=darkgreen)
        self.list_frame = tkinter.Frame(self.friendrequest_popup, bg=darkgreen)
        self.button_frame = tkinter.Frame(self.friendrequest_popup, bg=darkgreen)

        self.label_frame.pack(pady=5)
        self.list_frame.pack()
        self.button_frame.pack(pady=5)

        # Label Frame Layout
        self.label_test = tkinter.Label(self.label_frame, text="Friend Request", font=('haveltica', 18), fg=yellow,
                                        bg=darkgreen, width=20)
        self.label_test.grid(row=0, column=0, padx=5, pady=5)

        # List Frame Layout
        self.my_scrollbar = tkinter.Scrollbar(self.list_frame, orient=VERTICAL)
        self.my_listbox = tkinter.Listbox(self.list_frame, height=10, width=25, borderwidth=0, bg=white, fg=darkgreen,
                                          font=my_font, yscrollcommand=self.my_scrollbar.set)
        self.my_scrollbar.config(command=self.my_listbox.yview)
        self.my_listbox.grid(row=0, column=0)
        self.my_scrollbar.grid(row=0, column=1, sticky="NS")

        # Button Frame Layout
        self.accept_button = tkinter.Button(self.button_frame, text="Accept", width=10, borderwidth=0, font=my_font,
                                            bg=yellow, fg=black, command=lambda: self.accept())
        self.refuse_button = tkinter.Button(self.button_frame, text="Refuse", width=10, borderwidth=0, font=my_font,
                                            bg=yellow, fg=black, command=lambda: self.refuse())
        self.accept_button.grid(row=0, column=0, padx=5, pady=5)
        self.refuse_button.grid(row=0, column=1, padx=5, pady=5)

        self.update_displaylist()
        self.friendrequest_popup.protocol("WM_DELETE_WINDOW", self.close_confirm)

    def close_confirm(self):
        self.active = False
        self.friendrequest_popup.destroy()

    def bring_to_front(self):
        self.friendrequest_popup.lift()

    def update_friendlist(self, fr_list):
        self.friendrequest_list = fr_list
        self.update_displaylist()

    def update_displaylist(self):
        self.my_listbox.delete(0, END)
        for user in self.friendrequest_list:
            self.my_listbox.insert(0, user)
            self.my_listbox.itemconfig(0, {'fg': 'green2'})

    def accept(self):
        chosen = self.my_listbox.curselection()
        if len(chosen) == 0:
            showerror(title="No friend selected!",
                      message=f"Please choose a friend !")
        else:
            userid = self.my_listbox.get(chosen[0])
            self.server_sock.send(f"ACCEPT_FRIEND {userid}".encode(ENCODER))
            self.friendrequest_list.remove(userid)
            self.update_displaylist()

    def refuse(self):
        chosen = self.my_listbox.curselection()
        if len(chosen) == 0:
            showerror(title="No friend selected!",
                      message=f"Please choose a friend!")
        else:
            userid = self.my_listbox.get(chosen[0])
            self.server_sock.send(f"REFUSE_FRIEND {userid}".encode(ENCODER))
            self.friendrequest_list.remove(userid)
            self.update_displaylist()

if __name__ == "__main__":
    login_page = login_window()
    login_page.render()
