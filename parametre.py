from tkinter import *
from tkinter import ttk, messagebox
import tkinter as tk
import json

oWindows = tk.Tk()
oWindows.title("⚙️ Configuration des Paramètres")
oWindows.resizable(False, False)

style = ttk.Style(oWindows)
style.theme_use('clam')

frame = ttk.Frame(oWindows, padding=20)
frame.grid()

def quitter():
    oWindows.destroy()

def sauvegarder():
    params = {
        "serveur": entry_serveur.get(),
        "port": int(entry_port.get()),
        "utilisateur": entry_utilisateur.get(),
        "mot_de_passe": entry_mdp.get(),
    }
    with open("param.json", "w", encoding="utf-8") as f:
        json.dump(params, f, indent=4)
    messagebox.showinfo("Sauvegarde", "Paramètres enregistrés dans param.json")

# Champs
ttk.Label(frame, text="Serveur:").grid(row=0, column=0, sticky=W, pady=5)
entry_serveur = ttk.Entry(frame)
entry_serveur.grid(row=0, column=1, pady=5)
entry_serveur.insert(0, "localhost")

ttk.Label(frame, text="Port:").grid(row=1, column=0, sticky=W, pady=5)
entry_port = ttk.Entry(frame)
entry_port.grid(row=1, column=1, pady=5)
entry_port.insert(0, "3306")

ttk.Label(frame, text="Utilisateur:").grid(row=2, column=0, sticky=W, pady=5)
entry_utilisateur = ttk.Entry(frame)
entry_utilisateur.grid(row=2, column=1, pady=5)
entry_utilisateur.insert(0, "administrateur")

ttk.Label(frame, text="Mot de passe:").grid(row=3, column=0, sticky=W, pady=5)
entry_mdp = ttk.Entry(frame, show="*")
entry_mdp.grid(row=3, column=1, pady=5)
entry_mdp.insert(0, "secret")


ttk.Button(frame, text="Sauvegarder", command=sauvegarder).grid(row=5, column=0, columnspan=2, pady=10)
ttk.Button(frame, text="Quitter", command=quitter).grid(row=6, column=0, columnspan=2, pady=5)

oWindows.mainloop()