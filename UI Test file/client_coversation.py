# SIMPLE P2P CHAT - CONVERSATION
import tkinter, socket, threading
from tkinter import DISABLED, VERTICAL, END, NORMAL
from theme import *

#define FRIEND LIST window
conver_page = tkinter.Tk()
conver_page.title("Simple P2P Chat application - Conversation")
conver_page.geometry("700x700")
conver_page.resizable(0,0)

#set window colors
conver_page.config(bg=darkgreen)

#Define GUI Layout
#Create Frames
info_frame = tkinter.Frame(conver_page, bg=yellow)
label_frame = tkinter.Frame(conver_page, bg = darkgreen)
input_frame = tkinter.Frame(conver_page, bg=white)
output_frame = tkinter.Frame(conver_page, bg=white)

info_frame.pack(pady = 10)
label_frame.pack(pady = 10)
output_frame.pack(pady = 10)
input_frame.pack()

# Info Frame Layout
name_label = tkinter.Label(info_frame, text = "User ID:", font=my_font, fg=darkgreen, bg=yellow, width= 10, anchor = "nw")
name = tkinter.Label(info_frame, text = "hoangtran12902", font=my_font, fg=darkgreen, bg=yellow, width=44, anchor = "nw")
mail_label = tkinter.Label(info_frame, text = "User Email:", font=my_font, fg=darkgreen, bg=yellow, width= 10, anchor = "nw")
mail = tkinter.Label(info_frame, text = "hoang.tran12902@gmail.com", font=my_font, fg=darkgreen, bg=yellow, width=44, anchor = "nw")

name_label.grid(row = 0 , column=0, padx = 5, pady = 5)
name.grid(row = 0 , column=1, columnspan= 2, padx = 5, pady = 5)
mail_label.grid(row = 1 , column=0, padx = 5, pady = 5)
mail.grid(row = 1 , column=1, columnspan= 2, padx = 5, pady = 5)

friend_list_label = tkinter.Label(label_frame, text = "Chatting with huyhoang0512", font=('haveltica', 18), fg=white, bg=darkgreen, width=44, anchor = "nw")
friend_list_label.grid(row = 0 , column=0, padx = 5, pady = 5)

#Output Frame Layout
my_scrollbar = tkinter.Scrollbar(output_frame, orient=VERTICAL)
my_listbox = tkinter.Listbox(output_frame, height=20, width=55, borderwidth=0, bg=white, fg=darkgreen, font=my_font, yscrollcommand=my_scrollbar.set)
my_scrollbar.config(command=my_listbox.yview)
my_listbox.grid(row=0, column=0)
my_scrollbar.grid(row=0, column=1, sticky="NS")

#Input Frame Layout
input_entry = tkinter.Entry(input_frame, width=39, borderwidth=0, font=my_font)
file_button = tkinter.Button(input_frame, text="File", borderwidth=0, width=7, font=my_font, bg=yellow, fg = black)
send_button = tkinter.Button(input_frame, text="Send", borderwidth=0, width=7, font=my_font, bg=yellow, fg = black)
input_entry.grid(row=0, column=0, padx=5, pady=5)
file_button.grid(row=0, column=1, padx=5, pady=5)
send_button.grid(row=0, column=2, padx=5, pady=5)

#Run the conver_page window's mainloop()
conver_page.mainloop()
