#imports
import tkinter as tk
from tkinter import filedialog

#config
minimum = 180
charpixel = 6

#functions
def ask_string(title, label):
    result = {"value": None}

    text_size = len(label) * charpixel
    size = minimum + text_size

    def submit():
        result["value"] = entry.get()
        root.destroy()

    root = tk.Tk()
    root.title(title)
    root.geometry(f"{size}x120")
    root.resizable(False, False)

    #center window
    root.update_idletasks()
    w = root.winfo_width()
    h = root.winfo_height()
    x = (root.winfo_screenwidth() - w) // 2
    y = (root.winfo_screenheight() - h) // 2
    root.geometry(f"{w}x{h}+{x}+{y}")

    tk.Label(root, text=label, font=("Arial", 12)).pack(pady=10)
    entry = tk.Entry(root, font=("Arial", 14))
    entry.pack(padx=20, fill="x")
    entry.focus()

    entry.bind("<Return>", lambda event: submit())

    tk.Button(root, text="OK", command=submit).pack(pady=10)

    root.mainloop()

    return result["value"]
def ask_yes_no(title, message):
    result = {"value": False}

    text_size = len(message) * charpixel
    size = minimum + text_size

    def yes():
        result["value"] = True
        root.destroy()

    def no():
        root.destroy()
        
    root = tk.Tk()
    root.title(title)
    root.geometry(f"{size}x90")
    root.resizable(False, False)

    # center window
    root.update_idletasks()
    w = root.winfo_width()
    h = root.winfo_height()
    x = (root.winfo_screenwidth() - w) // 2
    y = (root.winfo_screenheight() - h) // 2
    root.geometry(f"{w}x{h}+{x}+{y}")

    tk.Label(root, text=message, font=("Arial", 12)).pack(pady=10)

    frame = tk.Frame(root)
    frame.pack(pady=(5, 0))

    tk.Button(frame, text="Yes", width=10, command=yes).pack(side="left", padx=10)
    tk.Button(frame, text="No", width=10, command=no).pack(side="right", padx=10)

    # keyboard support
    root.bind("<Return>", lambda e: yes())
    root.bind("<Escape>", lambda e: no())

    root.mainloop()

    return result["value"]
def notify(title, label):
    def close():
        root.destroy()

    text_size = len(label) * int(charpixel // 1.5)
    size = minimum + text_size

    root = tk.Tk()
    root.title(title)
    root.geometry(f"{size}x85")
    root.resizable(False, False)

    #center window
    root.update_idletasks()
    w = root.winfo_width()
    h = root.winfo_height()
    x = (root.winfo_screenwidth() - w) // 2
    y = (root.winfo_screenheight() - h) // 2
    root.geometry(f"{w}x{h}+{x}+{y}")

    tk.Label(root, text=label, font=("Arial", 12)).pack(padx=10, pady=(10, 10))
    tk.Button(root, text="OK", command=close).pack(pady=(0, 10))

    root.bind("<Return>", lambda event: close())

    root.mainloop()

def ask_file_open(title, initial_dir=".", filetypes=(("Text files", "*.txt"),)):
    result = {"value": None}

    def choose():
        result["value"] = filedialog.askopenfilename(
            title=title,
            initialdir=initial_dir,
            filetypes=filetypes
        )
        root.destroy()

    root = tk.Tk()
    root.withdraw()
    root.after(0, choose)
    root.mainloop()

    return result["value"]
def ask_file_save(title, initial_dir=".", filetypes=(("Text files", "*.txt"),), defaultextension=".txt"):
    result = {"value": None}

    def choose():
        result["value"] = filedialog.asksaveasfilename(
            title=title,
            initialdir=initial_dir,
            filetypes=filetypes,
            defaultextension=defaultextension
        )
        root.destroy()

    root = tk.Tk()
    root.withdraw()
    root.after(0, choose)
    root.mainloop()

    return result["value"]

def ask_promo(title, message):
    result = {"value": None}

    text_size = len(message) * charpixel
    size = minimum + text_size

    def queen():
        result["value"] = "queen"
        root.destroy()
    def rook():
        result["value"] = "rook"
        root.destroy()
    def bishop():
        result["value"] = "bishop"
        root.destroy()
    def knight():
        result["value"] = "knight"
        root.destroy()
        
    root = tk.Tk()
    root.title(title)
    root.geometry(f"{size+100}x90")
    root.resizable(False, False)

    # center window
    root.update_idletasks()
    w = root.winfo_width()
    h = root.winfo_height()
    x = (root.winfo_screenwidth() - w) // 2
    y = (root.winfo_screenheight() - h) // 2
    root.geometry(f"{w}x{h}+{x}+{y}")

    tk.Label(root, text=message, font=("Arial", 12)).pack(pady=10)

    frame = tk.Frame(root)
    frame.pack(pady=(5, 0))

    tk.Button(frame, text="Queen", width=10, command=queen).pack(side="left", padx=5)
    tk.Button(frame, text="Rook", width=10, command=rook).pack(side="left", padx=5)
    tk.Button(frame, text="Bishop", width=10, command=bishop).pack(side="right", padx=5)
    tk.Button(frame, text="Knight", width=10, command=knight).pack(side="right", padx=5)

    root.mainloop()

    return result["value"]