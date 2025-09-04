from tkinter import *
from tkinter import ttk, messagebox
import tkinter as tk
import json

oWindows = tk.Tk()
oWindows.title("⚙️ Configuration des Paramètres")
oWindows.geometry("400x600")  # Fenêtre plus grande
oWindows.resizable(False, False)
oWindows.configure(bg="#f0f0f0")



style = ttk.Style(oWindows)
style.theme_use('clam')
style.configure("Gray.TFrame", background="#f0f0f0")

frame = ttk.Frame(oWindows, padding=40)  # Plus de padding
frame.place(relx=0.5, rely=0.5, anchor="center")  # Centre le frame
frame.configure(style="Gray.TFrame")

def quitter():
    oWindows.destroy()

with open("param.json", "r", encoding="utf-8") as f:
    params = json.load(f)



def sauvegarder():
    params = {
        "host": entry_host.get(),
        "user": entry_user.get(),
        "password": entry_pswd.get(),
        "database": entry_db.get(),
        "chemin_fichier": entry_path.get()
    }
    with open("param.json", "w", encoding="utf-8") as f:
        json.dump(params, f, indent=4)
    messagebox.showinfo("Sauvegarde", "Paramètres enregistrés dans param.json")

# Champs
ttk.Label(frame, text="host:").grid(row=0, column=0, sticky=W, pady=10)
entry_host = ttk.Entry(frame)
entry_host.grid(row=0, column=1, pady=10)
entry_host.insert(0, params["host"])

ttk.Label(frame, text="user:").grid(row=1, column=0, sticky=W, pady=10)
entry_user = ttk.Entry(frame)
entry_user.grid(row=1, column=1, pady=10)
entry_user.insert(0, params["user"])

ttk.Label(frame, text="password:").grid(row=2, column=0, sticky=W, pady=10)
entry_pswd = ttk.Entry(frame, show="*")
entry_pswd.grid(row=2, column=1, pady=10)
entry_pswd.insert(0, params["password"])

ttk.Label(frame, text="database:").grid(row=3, column=0, sticky=W, pady=10)
entry_db = ttk.Entry(frame)
entry_db.grid(row=3, column=1, pady=10)
entry_db.insert(0, params["database"])

ttk.Label(frame, text="chemin d'acces:").grid(row=3, column=0, sticky=W, pady=10)
entry_path = ttk.Entry(frame)
entry_path.grid(row=3, column=1, pady=10)
entry_path.insert(0, params["chemin_fichier"])


ttk.Button(frame, text="Sauvegarder", command=sauvegarder).grid(row=5, column=0, columnspan=2, pady=20)
ttk.Button(frame, text="Quitter", command=quitter).grid(row=6, column=0, columnspan=2, pady=10)

oWindows.mainloop()