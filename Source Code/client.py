# Client Chat App
import tkinter, socket, threading
from tkinter import *
from tkinter import messagebox
from theme import *

# Defining constant
S_HOSTNAME = "localhost"
S_IP = socket.gethostbyname(S_HOSTNAME)
S_PORT = 50000
ACC_SERVER = (S_IP, S_PORT)
MY_PORT = 50001
LISTEN_ADDRESS = ('localhost', MY_PORT)
ENCODER = 'utf-8'
BYTESIZE = 1024

# Defining global variable
global myID
global password
friend_list: dict
global server_sock
global listen_sock
sock_list: dict
global login_win
global friendlist_win
conversation_window: dict

class login_window:
    def __init__(self):
        #define Login window
        self.login_page = tkinter.Tk()
        self.login_page.title("Simple P2P Chat application - Login")
        self.login_page.geometry("600x300")
        self.login_page.resizable(0,0)

        #set windows colors
        self.login_page.config(bg=darkgreen)

        #Define GUI Layout
        #Create Frames
        self.login_frame = tkinter.Frame(self.login_page, bg=darkgreen)

        self.login_frame.pack(pady= 30)

        #Frame Layout
        self.login_label = tkinter.Label(self.login_frame, text="Login", font=("haveltica", 18), fg=yellow, bg=darkgreen)
        self.uid_label = tkinter.Label(self.login_frame, text="User ID:", font=my_font, fg=yellow, bg=darkgreen)
        self.uid_entry = tkinter.Entry(self.login_frame, borderwidth=0, font=my_font)
        self.pw_label = tkinter.Label(self.login_frame, text="Password:", font=my_font, fg=yellow, bg=darkgreen)
        self.pw_entry = tkinter.Entry(self.login_frame, borderwidth=0, font=my_font, show = '*')
        self.signin_button = tkinter.Button(self.login_frame, text="Sign in", font=my_font, fg = black, bg=yellow, borderwidth=0, width=10, height=3, command = lambda: self.check_fields())
        self.register_button = tkinter.Button(self.login_frame, text="Register", font=my_font_small, fg = white, bg=lightgreen, borderwidth=0, width=8)
        self.forgotpw_button = tkinter.Button(self.login_frame, text="Forgot password", font=my_font_small, fg = white, bg=lightgreen, borderwidth=0, width= 16)
        self.showpasswd_button = tkinter.Checkbutton(self.login_frame, text="Show password", font=my_font_small, fg="orange", bg = darkgreen, activebackground=darkgreen, command = lambda: self.show_passwd(self.pw_entry), anchor = 'w')

        self.login_label.grid(row = 0, column = 0, columnspan = 4, padx = 2, pady = 10)
        self.uid_label.grid(row=1, column=0, padx=2, pady=5)
        self.uid_entry.grid(row=1, column=1, columnspan= 2, padx=2, pady=5)
        self.pw_label.grid(row=2, column=0, padx=2, pady=5)
        self.pw_entry.grid(row=2, column=1, columnspan= 2, padx=2, pady=5)
        self.signin_button.grid(row=1, column=3, rowspan = 2, padx=10, pady=5)
        self.showpasswd_button.grid(row = 3, column=1, columnspan = 2, padx = 10, pady = 5)
        self.register_button.grid(row=4, column=1, padx=10, pady=5)
        self.forgotpw_button.grid(row=4, column=2, padx=10, pady=5)

    def show_passwd(self, entry_field):
        if entry_field.cget('show') == '*':
            entry_field.config(show='')
        else:
            entry_field.config(show='*')

    def check_fields(self):
        if self.uid_entry.get() == "" or self.pw_entry == "":
            self.pop_up("Missing field(s)!", "Please fill in every field(s)!")
        else:
            login()

    def pop_up(self, title, message):
        messagebox.showinfo(title, message)

    def close(self):
        self.login_page.quit()

    def render(self):
        self.login_page.mainloop()


class frlist_window:
    def __init__(self, onlinelist, offlinelist):
        self.updatelist(onlinelist, offlinelist)

        #define FRIEND LIST window
        self.flist_page = tkinter.Tk()
        self.flist_page.title("Simple P2P Chat application - Friends List")
        self.flist_page.geometry("700x800")
        self.flist_page.resizable(0,0)

        #set window colors
        self.flist_page.config(bg=darkgreen)

        #Define GUI Layout
        #Create Frames
        self.info_frame = tkinter.Frame(self.flist_page, bg=yellow)
        self.label_frame = tkinter.Frame(self.flist_page, bg = darkgreen)
        self.search_frame = tkinter.Frame(self.flist_page, bg=white)
        self.list_frame = tkinter.Frame(self.flist_page, bg=white)
        self.button_frame = tkinter.Frame(self.flist_page, bg = white)
        

        self.info_frame.pack(pady = 15)
        self.label_frame.pack(pady = 0)
        self.search_frame.pack(pady = 10)
        self.list_frame.pack()
        self.button_frame.pack(pady = 5)

        # Info Frame Layout
        self.name_label = tkinter.Label(self.info_frame, text = "User ID:", font=my_font, fg=darkgreen, bg=yellow, width= 10, anchor = "nw")
        self.name = tkinter.Label(self.info_frame, text = "hoangtran12902", font=my_font, fg=darkgreen, bg=yellow, width=44, anchor = "nw")
        self.mail_label = tkinter.Label(self.info_frame, text = "User Email:", font=my_font, fg=darkgreen, bg=yellow, width= 10, anchor = "nw")
        self.mail = tkinter.Label(self.info_frame, text = "hoang.tran12902@gmail.com", font=my_font, fg=darkgreen, bg=yellow, width=44, anchor = "nw")

        self.name_label.grid(row = 0 , column=0, padx = 5, pady = 5)
        self.name.grid(row = 0 , column=1, columnspan= 2, padx = 5, pady = 5)
        self.mail_label.grid(row = 1 , column=0, padx = 5, pady = 5)
        self.mail.grid(row = 1 , column=1, columnspan= 2, padx = 5, pady = 5)

        #Label Frame Layout
        self.friend_list_label = tkinter.Label(self.label_frame, text = "Friend List", font=('haveltica', 18), fg=white, bg=darkgreen, width= 30, anchor = "nw")
        self.frrequest_button = tkinter.Button(self.label_frame, text = "Friend request", borderwidth = 0, width = 10, font = my_font_small, bg = yellow, fg = black)
        self.addfr_button = tkinter.Button(self.label_frame, text = "Add friend", borderwidth = 0, width = 10, font = my_font_small, bg = yellow, fg = black)
        self.friend_list_label.grid(row = 0 , column=0, padx = 5, pady = 5)
        self.frrequest_button.grid(row = 0 , column=1, padx = 5, pady = 5)
        self.addfr_button.grid(row = 0 , column=2, padx = 5, pady = 5)

        #List Frame Layout
        self.my_scrollbar = tkinter.Scrollbar(self.list_frame, orient=VERTICAL)
        self.my_listbox = tkinter.Listbox(self.list_frame, height=20, width=55, borderwidth=0, bg=white, fg=darkgreen, font=my_font, yscrollcommand=self.my_scrollbar.set)
        self.my_scrollbar.config(command=self.my_listbox.yview)
        self.my_listbox.grid(row=0, column=0)
        self.my_scrollbar.grid(row=0, column=1, sticky="NS")

        #Search Frame Layout
        self.input_entry = tkinter.Entry(self.search_frame, width=44, borderwidth=0, font=my_font)
        self.search_button = tkinter.Button(self.search_frame, text="Search", borderwidth=0, width=10, font=my_font, bg=yellow, fg = black)
        self.input_entry.grid(row=0, column=0, padx=5, pady=5)
        self.search_button.grid(row=0, column=1, padx=5, pady=5)
        self.input_entry.bind("<KeyRelease>", self.search_check)
        self.search_button.bind("<Button-1>", self.search_check)

        #Button Frame Layout
        self.unfriend_button = tkinter.Button(self.button_frame, text = "Unfriend", width=27, borderwidth = 0, font = my_font, bg = yellow, fg = black)
        self.chat_button = tkinter.Button(self.button_frame, text = "Start chatting", width = 27, borderwidth = 0, font = my_font, bg = yellow, fg = black)
        self.unfriend_button.grid(row=0, column=0,padx=5, pady=5)
        self.chat_button.grid(row=0, column=1, padx=5, pady=5)
        self.update_displaylist(self.onlinelist, self.offlinelist)

    def updatelist(self, onlinelist, offlinelist):
        self.onlinelist = onlinelist
        self.offlinelist = offlinelist

    def search_check(self, event):
        typed = self.input_entry.get()
        if type == '':
            self.update_displaylist(self.onlinelist, self.offlinelist)
        else:
            online_tmplist = []
            offline_tmplist = []
            for user in  self.onlinelist:
                if typed.lower() in user.lower():
                    online_tmplist.append(user)
            for user in self.offlinelist:
                if typed.lower() in user.lower():
                    offline_tmplist.append(user)
            self.update_displaylist(online_tmplist, offline_tmplist)

    def update_displaylist(self, onlinelist, offlinelist):
        self.my_listbox.delete(0, END)
        for user in onlinelist:
            self.my_listbox.insert(0, user)
            self.my_listbox.itemconfig(0,{'fg':'green2'})
        for user in offlinelist:
            self.my_listbox.insert(END, user)
            self.my_listbox.itemconfig(END,{'fg':'gray63'})

    def render(self):
        #Run the self.flist_page window's mainloop()
        self.flist_page.mainloop()

class conversation_window:
    def __init__(self, root):
        #define CONVERSATION window
        self.comver_page = tkinter.Toplevel(root)
        self.comver_page.title("Simple P2P Chat application - Conversation")
        self.comver_page.geometry("700x700")
        self.comver_page.resizable(0,0)

        #set window colors
        self.comver_page.config(bg=darkgreen)

        #Define GUI Layout
        #Create Frames
        self.info_frame = tkinter.Frame(self.comver_page, bg=yellow)
        self.label_frame = tkinter.Frame(self.comver_page, bg = darkgreen)
        self.input_frame = tkinter.Frame(self.comver_page, bg=white)
        self.output_frame = tkinter.Frame(self.comver_page, bg=white)

        self.info_frame.pack(pady = 10)
        self.label_frame .pack(pady = 10)
        self.output_frame.pack(pady = 10)
        self.input_frame.pack()

        # Info Frame Layout
        self.name_label = tkinter.Label(self.info_frame, text = "User ID:", font=my_font, fg=darkgreen, bg=yellow, width= 10, anchor = "nw")
        self.name = tkinter.Label(self.info_frame, text = "hoangtran12902", font=my_font, fg=darkgreen, bg=yellow, width=44, anchor = "nw")
        self.mail_label = tkinter.Label(self.info_frame, text = "User Email:", font=my_font, fg=darkgreen, bg=yellow, width= 10, anchor = "nw")
        self.mail = tkinter.Label(self.info_frame, text = "hoang.tran12902@gmail.com", font=my_font, fg=darkgreen, bg=yellow, width=44, anchor = "nw")

        self.name_label.grid(row = 0 , column=0, padx = 5, pady = 5)
        self.name.grid(row = 0 , column=1, columnspan= 2, padx = 5, pady = 5)
        self.mail_label.grid(row = 1 , column=0, padx = 5, pady = 5)
        self.mail.grid(row = 1 , column=1, columnspan= 2, padx = 5, pady = 5)

        self.friend_list_label = tkinter.Label(self.label_frame , text = "Chatting with huyhoang0512", font=('haveltica', 18), fg=white, bg=darkgreen, width=44, anchor = "nw")
        self.friend_list_label.grid(row = 0 , column=0, padx = 5, pady = 5)

        #Output Frame Layout
        self.my_scrollbar = tkinter.Scrollbar(self.output_frame, orient=VERTICAL)
        self.my_listbox = tkinter.Listbox(self.output_frame, height=20, width=55, borderwidth=0, bg=white, fg=darkgreen, font=my_font, yscrollcommand=self.my_scrollbar.set)
        self.my_scrollbar.config(command=self.my_listbox.yview)
        self.my_listbox.grid(row=0, column=0)
        self.my_scrollbar.grid(row=0, column=1, sticky="NS")

        #Input Frame Layout
        self.input_entry = tkinter.Entry(self.input_frame, width=39, borderwidth=0, font=my_font)
        self.file_button = tkinter.Button(self.input_frame, text="File", borderwidth=0, width=7, font=my_font, bg=yellow, fg = black)
        self.send_button = tkinter.Button(self.input_frame, text="Send", borderwidth=0, width=7, font=my_font, bg=yellow, fg = black)
        self.input_entry.grid(row=0, column=0, padx=5, pady=5)
        self.file_button.grid(row=0, column=1, padx=5, pady=5)
        self.send_button.grid(row=0, column=2, padx=5, pady=5)

    def render(self):
        #Run the self.comver_page window's mainloop()
        self.comver_page.mainloop()

def login():
    global myID, password, friend_list, server_sock, login_win, friendlist_win
    myID = login_win.uid_entry.get()
    password = login_win.pw_entry.get()
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.connect(ACC_SERVER)
    server_sock.send(f"s l {myID} {password}".encode(ENCODER))
    response = server_sock.recv(BYTESIZE).decode(ENCODER)
    if (response == "FAIL"):
        login_win.pop_up("Login failed!", "Incorrect User ID or Password!")
    else:
        listen_frlist_update()
        login_win.close()
        onlinelist = []
        offlinelist = []
        for userid in friend_list:
            if friend_list[userid] == ('NULL', 'NULL'):
                offlinelist.append(userid)
            else:
                onlinelist.append(userid)
        friendlist_win = frlist_window(onlinelist, offlinelist)

def listen_frlist_update():
    global friend_list, server_sock
    friend_name = server_sock.recv(BYTESIZE).decode(ENCODER).split(' ')
    friend_ip = server_sock.recv(BYTESIZE).decode(ENCODER).split(' ')
    friend_port = server_sock.recv(BYTESIZE).decode(ENCODER).split(' ')
    for i in range(len(friend_name)):
        friend_list[friend_name[i]] = (friend_ip[i], friend_port[i])

def log_out():
    pass

def find_user():
    pass

def request_friend():
    pass

def unfriend():
    pass

def register():
    pass

def forgot_password():
    pass

def listen_to_friend():
    global listen_sock
    listen_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listen_sock.bind(LISTEN_ADDRESS)
    listen_sock.listen()

    # Verify and Accept or Deny Connection
    while True:
        connected_client, address = listen_sock.accept()
        connected_ID = check_address(address)
        if (connected_ID != "NULL"):
            sock_list[connected_ID] = connected_client
            #print("Connected with {}".format(str(address)))
            receive_thread = threading.Thread(target=recieve_message, args=(connected_client,connected_ID,))
            receive_thread.start()
            send_thread = threading.Thread(target=send_message, args=(connected_client,))
            send_thread.start()
        else:
            connected_client.close()

def recieve_message(connected_client, client_ID):
    while True:
        type, message = connected_client.recv(BYTESIZE).decode(ENCODER).split(' ')
        if (type == 'm'):
            message = '{}: {}'.format(client_ID, message)
            print(message)
        else:
            pass

def send_message(connected_client, message):
    message = '{} {}'.format('m', message)
    connected_client.send(message.encode(ENCODER))

def send_file(connected_client):
    pass

def connect_to_friend(friend_ID):
    global sock_list
    sock_list[friend_ID] = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock_list[friend_ID].connect(friend_list[friend_ID])
    receive_thread = threading.Thread(target=recieve_message, args=(sock_list[friend_ID],friend_ID,))
    receive_thread.start()
    send_thread = threading.Thread(target=send_message, args=(sock_list[friend_ID],))
    send_thread.start()


def check_address(address):
    for userid in friend_list:
        if friend_list[userid] == address:
            return userid
    return "NULL"

login_win = login_window()
#conversation_win = conversation_window(login_win.login_page)
#login_win.render()

