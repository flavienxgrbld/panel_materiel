import tkinter as tk
from tkinter import ttk
import subprocess

import tkinter.messagebox as messagebox

def quitter(): 
    oWindows.destroy()


def verif_requirements():
    try:
        subprocess.run(["pip", "install", "-r", "requirements.txt"], check=True)
        messagebox.showinfo("Succès", "Les requirements sont installés.")
        # Affiche les autres boutons
        btn_interface1.grid(column=0, row=0, padx=10, pady=10)
        btn_interface2.grid(column=1, row=0, padx=10, pady=10)

    except subprocess.CalledProcessError as e:
        messagebox.showerror("Erreur", f"Échec installation requirements:\n{e}")

def gestion_materiel():
    try:
        subprocess.run(["python", "gestion-materiel.py"], check=True)
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Erreur", f"Échec lancement gestion-materiel.py:\n{e}")

def fiche_remise_materiel():
    try:
        subprocess.run(["python", "remise-materiel.py"], check=True)
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Erreur", f"Échec lancement remise-materiel.py:\n{e}")


oWindows = tk.Tk()
oWindows.title("🖥️ Centre de Contrôle des Opérations")
oWindows.resizable(False, False)

style = ttk.Style(oWindows)
style.theme_use('clam')

frame = ttk.Frame(oWindows, padding=50)
frame.grid()


btn_quitter = ttk.Button(oWindows, text="Quitter", command=quitter)
btn_quitter.place(relx=1.0, rely=0.0, anchor="ne", x=-10, y=10)

btn_requirements = ttk.Button(frame, text="Vérif Requirements", command=verif_requirements)
btn_requirements.grid(column=2, row=0, padx=10, pady=10)

btn_interface1 = ttk.Button(frame, text="Gestion De Materiel", command=gestion_materiel)
btn_interface2 = ttk.Button(frame, text="Fiche Remise Materiel", command=fiche_remise_materiel)

oWindows.mainloop()