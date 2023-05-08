# SIMPLE P2P CHAT - CONVERSATION
import tkinter, socket, threading
from tkinter import DISABLED, VERTICAL, END, NORMAL
from theme import *
from tkinter import messagebox
from tkinter.messagebox import askyesno, showerror
from tkinter import filedialog

# Defining constant
S_HOSTNAME = "localhost"
S_IP = socket.gethostbyname(S_HOSTNAME)
S_PORT = 50000
ACC_SERVER = (S_IP, S_PORT)
MY_PORT = 50001
LISTEN_ADDRESS = ('localhost', MY_PORT)
ENCODER = 'utf-8'
BYTESIZE = 1024


class forgotPassword_window:
    def __init__(self):
        #define FORGOT PASSWORD window
        self.forgotpw_page = tkinter.Tk()
        self.forgotpw_page.title("Forgot Password")
        self.forgotpw_page.geometry("300x450")
        self.forgotpw_page.resizable(0, 0)

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
        server_sock.send(f"FORGOTPASS {userId}:{email}:{password}".encode(ENCODER))
        response = server_sock.recv(BYTESIZE).decode(ENCODER)
        if response == 'FAIL_UserID':
            messagebox.showerror("Error!", "User ID does not exist!")
        elif response == 'FAIL_EMAIL':
            messagebox.showerror("Error!", "Email is Uncorrected!")
        else:
            # frlist_window(userId, password, email, {}, server_sock)
            self.forgotpw_page.destroy()

    def close_confirm(self):
        confirm_reply = askyesno(title="Cancel?", message="Do you want to cancel?")
        if confirm_reply:
            # login_window()
            self.register_page.destroy()


    def render(self):
        self.forgotpw_page.mainloop()


test = forgotPassword_window()
test.render()