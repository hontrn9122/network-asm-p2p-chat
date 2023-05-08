# SIMPLE P2P CHAT - CONVERSATION
import tkinter, socket, threading
from theme import *
from tkinter import messagebox
from tkinter.messagebox import askyesno

# Defining constant
S_HOSTNAME = "localhost"
S_IP = socket.gethostbyname(S_HOSTNAME)
S_PORT = 50000
ACC_SERVER = (S_IP, S_PORT)
MY_PORT = 50001
LISTEN_ADDRESS = ('localhost', MY_PORT)
ENCODER = 'utf-8'
BYTESIZE = 1024

class register_window:
    def __init__(self):
        #define REGISTER window
        self.register_page = tkinter.Tk()
        self.register_page.title("Register Account")
        self.register_page.geometry("300x450")
        self.register_page.resizable(0, 0)

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
        server_sock.send(f"REGISTER {userId}:{email}:{password}".encode(ENCODER))
        response = server_sock.recv(BYTESIZE).decode(ENCODER)
        if response == 'FAIL':
            messagebox.showerror("Register failed!", "User ID or Email already exists!")
        else:
            # frlist_window(userId, password, email, {}, server_sock)
            self.register_page.quit()


    def close_confirm(self):
        confirm_reply = askyesno(title="Cancel register?", message="Do you want cancel your register?")
        if confirm_reply:
            login_window()
            self.register_page.destroy()

    def render(self):
        self.register_page.mainloop()


test = register_window()
test.render()