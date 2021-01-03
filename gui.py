import functools
from os import path, listdir
import tkinter as tk
from tkinter import *
from tkinter import scrolledtext, filedialog
from tkinter.ttk import *
from main import posTagging

window = Tk()
window.title('English POS Tagging')
var = tk.StringVar()

ffont = ('bold', 30)
log = Frame(window)
log_txt = scrolledtext.ScrolledText(log, height=5, font=ffont)

# log.pack(expand=True, fill='both')
# log_txt.pack(expand=True, fill='both')


def get_entry(): 
    row = tk.Frame(window)
    lab = tk.Label(row, width=22, text='Input'+": ", anchor='w')
    ent = tk.Entry(row, width = 40)
    row.pack(side=tk.TOP, 
                fill=tk.X, 
                padx=10, 
                pady=10)
    lab.pack(side=tk.LEFT)
    ent.pack(side=tk.RIGHT, 
                expand=tk.YES, 
                fill=tk.X)
    log.pack(expand=True, fill='both')
    log_txt.pack(expand=True, fill='both')
    return ent

def show(ent, log):
    log.clipboard_clear()
    result = posTagging(ent)
    log.insert(INSERT, result)
    log.insert(INSERT, '\n')

if __name__ == '__main__':
    ent = get_entry()
    # print(ent)
    b1 = tk.Button(window, text='Get result',
           command=(lambda e=ent: show(e, log_txt)))
    b1.pack(side=tk.LEFT, padx=5, pady=5)
    window.mainloop()


window.mainloop()