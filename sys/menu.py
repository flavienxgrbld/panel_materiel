import tkinter as tk
from tkinter import ttk
import subprocess
import time
import tkinter.messagebox as messagebox
import os
import sys


current_dir = os.path.dirname(os.path.abspath(__file__))  # = panel_materiel/
requirements_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "requirements.txt")



def quitter(): 
    oWindows.destroy()


def verif_requirements():
    # Récupère le chemin absolu du dossier contenant ce fichier
    base_dir = os.path.dirname(os.path.abspath(__file__))
    requirements_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "requirements.txt")

    loading_label.grid(column=0, row=2, padx=10, pady=5)
    oWindows.update_idletasks()
    try:
        # Installation requirements
        subprocess.run(['pip', 'install', '-r', requirements_path], check=True)

        # Vérification des fichiers nécessaires
        missing = []
        for fname in ["gestion-materiel.py", "remise-materiel.py", "param.json"]:
            full_path = os.path.join(base_dir, fname)
            if not os.path.isfile(full_path):
                missing.append(fname)

        if missing:
            loading_label.grid_remove()
            error_label = ttk.Label(
                frame,
                text=f"❌ Erreur de chargement\nFichier(s) manquant(s) : {', '.join(missing)}",
                foreground="red"
            )
            error_label.grid(column=0, row=2, padx=10, pady=5)
            oWindows.update_idletasks()
            time.sleep(5)
            error_label.grid_remove()
            return

        # Mise à jour de l'interface
        btn_requirements.grid_remove()
        valid_label.grid(column=0, row=2, padx=10, pady=5)
        oWindows.update_idletasks()
        time.sleep(5)
        valid_label.grid_remove()

        btn_interface1.grid(column=0, row=0, padx=10, pady=10)
        btn_interface2.grid(column=1, row=0, padx=10, pady=10)
        btn_parametres.grid(column=2, row=0, padx=10, pady=10)
        btn_commande.grid(column=1, row=1, padx=10, pady=10)

    except subprocess.CalledProcessError as e:
        messagebox.showerror("Erreur", f"Échec de l'installation des requirements:\n{e}")

    loading_label.grid_remove()

def bypass_verif():
    btn_requirements.grid_remove()
    btn_bypass.grid_remove()
    btn_interface1.grid(column=0, row=0, padx=10, pady=10)
    btn_interface2.grid(column=1, row=0, padx=10, pady=10)
    btn_parametres.grid(column=2, row=0, padx=10, pady=10)
    btn_commande.grid(column=1, row=1, padx=10, pady=10)




def launcher_parametres():
    try:
        parametre_path = os.path.join(current_dir, "parametre.py")
        subprocess.Popen([sys.executable, parametre_path])
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Erreur", f"Échec lancement parametre.py:\n{e}")

def launcher_gestion_materiel():
    try:
        gestion_path = os.path.join(current_dir, "gestion-materiel.py")
        subprocess.Popen([sys.executable, gestion_path])
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Erreur", f"Échec lancement gestion-materiel.py:\n{e}")

def launcher_remise_materiel():
    try:
        remise_path = os.path.join(current_dir, "remise-materiel.py")
        subprocess.Popen([sys.executable, remise_path], cwd=current_dir)
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Erreur", f"Échec lancement remise-materiel.py:\n{e}")


def launcher_commande():
    try:
        commande_path = os.path.join(current_dir, "commande.py")  # ou autre script ?
        subprocess.Popen([sys.executable, commande_path])
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Erreur", f"Échec lancement commande.py:\n{e}")


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


btn_interface1 = ttk.Button(frame, text="Gestion De Materiel", command=launcher_gestion_materiel)
btn_interface2 = ttk.Button(frame, text="Fiche Remise Materiel", command=launcher_remise_materiel)

btn_parametres = ttk.Button(frame, text="Paramètres", command=launcher_parametres)
btn_commande = ttk.Button(frame, text="gestionnaire de commande", command=launcher_commande)

btn_bypass = ttk.Button(frame, text="bypass", command=bypass_verif)
btn_bypass.grid(column=0, row=3, padx=1, pady=1)

oWindows.mainloop()