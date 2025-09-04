import tkinter as tk
from tkinter import ttk
import subprocess
import time
import tkinter.messagebox as messagebox

def quitter(): 
    oWindows.destroy()


def verif_requirements():
    loading_label.grid(column=0, row=2, padx=10, pady=5)
    oWindows.update_idletasks()
    try:
        subprocess.run(["pip", "install", "-r", "requirements.txt"], check=True)
        loading_label.grid_remove()
        btn_requirements.grid_remove()
        valid_label.grid(column=0, row=2, padx=10, pady=5)
        oWindows.update_idletasks()
        time.sleep(2)
        valid_label.grid_remove()
        btn_interface1.grid(column=0, row=0, padx=10, pady=10)
        btn_interface2.grid(column=1, row=0, padx=10, pady=10)
        btn_parametres.grid(column=1, row=1, padx=10, pady=10)
        
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Erreur", f"Échec installation requirements:\n{e}")
        loading_label.grid_remove()


def ouvrir_parametres():
    messagebox.showinfo("Paramètres", "Ici, vous pouvez ajouter vos paramètres.")


def gestion_materiel():
    try:
        subprocess.Popen(["python", "gestion-materiel.py"])
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Erreur", f"Échec lancement gestion-materiel.py:\n{e}")

def fiche_remise_materiel():
    try:
        subprocess.Popen(["python", "remise-materiel.py"])
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
btn_requirements.grid(column=0, row=1, padx=10, pady=10)

loading_label = ttk.Label(frame, text="⏳ Chargement...", foreground="blue")
valid_label = ttk.Label(frame, text="✅ Chargement validé", foreground="green")

btn_interface1 = ttk.Button(frame, text="Gestion De Materiel", command=gestion_materiel)
btn_interface2 = ttk.Button(frame, text="Fiche Remise Materiel", command=fiche_remise_materiel)

btn_parametres = ttk.Button(frame, text="Paramètres", command=ouvrir_parametres)


oWindows.mainloop()