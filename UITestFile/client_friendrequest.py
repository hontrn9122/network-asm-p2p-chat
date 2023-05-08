# SIMPLE P2P CHAT - CONVERSATION
import tkinter, socket, threading
from tkinter import DISABLED, VERTICAL, END, NORMAL
from theme import *
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


class friendList_window:
    def __init__(self):
        self.friendrequest_list = []
        # define FRIEND LIST window
        self.friendrequest_popup = tkinter.Tk()
        self.friendrequest_popup.title("Friend Request")
        self.friendrequest_popup.geometry("300x350")
        self.friendrequest_popup.resizable(0, 0)

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
        self.label_test = tkinter.Label(self.label_frame, text="Friend Request", font=('haveltica', 18), fg=yellow, bg=darkgreen, width= 20)
        self.label_test.grid(row=0 , column=0, padx=5, pady=5)

        # List Frame Layout
        self.my_scrollbar = tkinter.Scrollbar(self.list_frame, orient=VERTICAL)
        self.my_listbox = tkinter.Listbox(self.list_frame, height=10, width=25, borderwidth=0, bg=white, fg=darkgreen, font=my_font, yscrollcommand=self.my_scrollbar.set)
        self.my_scrollbar.config(command=self.my_listbox.yview)
        self.my_listbox.grid(row=0, column=0)
        self.my_scrollbar.grid(row=0, column=1, sticky="NS")

        # Button Frame Layout
        self.accept_button = tkinter.Button(self.button_frame, text="Accept", width=10, borderwidth=0, font=my_font, bg=yellow, fg=black, command=lambda: self.accept())
        self.refuse_button = tkinter.Button(self.button_frame, text="Refuse", width=10, borderwidth=0, font=my_font, bg=yellow, fg=black, command=lambda: self.refuse())
        self.accept_button.grid(row=0, column=0, padx=5, pady=5)
        self.refuse_button.grid(row=0, column=1, padx=5, pady=5)
        # self.update_displaylist(self.friendrequest_list)

    def update_friendlist(self, list):
        self.friendrequest_list = list
        self.update_displaylist(self.friendrequest_list)

    def update_displaylist(self, friendrequest_list):
        self.my_listbox.delete(0, END)
        for user in friendrequest_list:
            self.my_listbox.insert(0, user)
            self.my_listbox.itemconfig(0, {'fg': 'green2'})

    def accept(self):
        chosen = self.my_listbox.curselection()
        if len(chosen) == 0:
            showerror(title="No friend selected!",
                      message=f"Please choose a friend !")
        else:
            pass

    def refuse(self):
        chosen = self.my_listbox.curselection()
        if len(chosen) == 0:
            showerror(title="No friend selected!",
                      message=f"Please choose a friend!")
        else:
            pass

    def render(self):
        self.friendrequest_popup.mainloop()

test = friendList_window()
test.render()