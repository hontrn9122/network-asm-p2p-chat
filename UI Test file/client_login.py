# SIMPLE P2P CHAT - LOGIN PAGE
import tkinter
from tkinter import *
from theme import *

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
        self.signin_button = tkinter.Button(self.login_frame, text="Sign in", font=my_font, fg = black, bg=yellow, borderwidth=0, width=10, height=3)
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

    def render(self):
        self.login_page.mainloop()

#login_page = login_window()
#login_page.render()



