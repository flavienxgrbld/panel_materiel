import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import os
import sys


# Dossiers & chemins
current_dir = os.path.dirname(os.path.abspath(__file__))  # = panel_materiel/
project_root = os.path.dirname(os.path.dirname(__file__))  # racine projet
requirements_path = os.path.join(project_root, "data", "requirements.txt")

# Liste des scripts à lancer
scripts = {
    "Gestion De Materiel": "gestion-materiel.py",
    "Fiche Remise Materiel": "remise-materiel.py",
    "Paramètres": "parametre.py",
    "Commande": "commande.py"
}


def quitter():
    oWindows.destroy()


def verif_requirements():
    # Afficher le label + barre de progression
    loading_label.grid(column=0, row=2, padx=10, pady=5)
    progressbar.grid(column=0, row=3, padx=10, pady=5)
    progressbar.start(10)  # animation

    oWindows.update_idletasks()

    oWindows.after(100, _do_verif)  # évite blocage de l'UI


def _do_verif():
    try:
        # Installation requirements
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "-r", requirements_path],
            check=True
        )

        # Vérification fichiers nécessaires
        files_to_check = {
            "gestion-materiel.py": current_dir,
            "remise-materiel.py": current_dir,
            "param.json": os.path.join(project_root, "data")  # ✅ param.json dans /data/
        }

        missing = []
        for fname, folder in files_to_check.items():
            if not os.path.isfile(os.path.join(folder, fname)):
                missing.append(fname)

        if missing:
            _stop_progress()
            error_label = ttk.Label(
                frame,
                text=f"❌ Erreur : fichiers manquants : {', '.join(missing)}",
                foreground="red"
            )
            error_label.grid(column=0, row=4, padx=10, pady=5)
            oWindows.after(5000, error_label.grid_remove)
            return

        # Succès
        _stop_progress()
        valid_label.grid(column=0, row=2, padx=10, pady=5)
        oWindows.after(2000, valid_label.grid_remove)  # auto-disparition

        afficher_boutons_scripts()

    except subprocess.CalledProcessError as e:
        _stop_progress()
        messagebox.showerror("Erreur", f"Échec de l'installation des requirements:\n{e}")


def _stop_progress():
    progressbar.stop()
    progressbar.grid_remove()
    loading_label.grid_remove()


def bypass_verif():
    btn_requirements.grid_remove()
    btn_bypass.grid_remove()
    afficher_boutons_scripts()


def afficher_boutons_scripts():
    btn_requirements.grid_remove()
    btn_bypass.grid_remove()

    # Placement auto des boutons
    col, row = 0, 0
    for name in scripts:
        ttk.Button(frame, text=name, command=lambda n=name: launcher(n)).grid(
            column=col, row=row, padx=10, pady=10
        )
        col += 1
        if col > 2:
            col = 0
            row += 1


def launcher(script_name):
    script_file = scripts[script_name]
    script_path = os.path.join(current_dir, script_file)

    if not os.path.isfile(script_path):
        messagebox.showerror("Erreur", f"Script introuvable : {script_file}")
        return

    try:
        subprocess.Popen([sys.executable, script_path], cwd=current_dir)
    except OSError as e:
        messagebox.showerror("Erreur", f"Échec lancement {script_file}:\n{e}")


# === Interface Tkinter ===
oWindows = tk.Tk()
oWindows.title("🖥️ Centre de Contrôle des Opérations")
oWindows.resizable(False, False)

style = ttk.Style(oWindows)
style.theme_use('clam')

frame = ttk.Frame(oWindows, padding=50)
frame.grid()

# Bouton quitter
btn_quitter = ttk.Button(oWindows, text="Quitter", command=quitter)
btn_quitter.place(relx=1.0, rely=0.0, anchor="ne", x=-10, y=10)

# Boutons initiaux
btn_requirements = ttk.Button(frame, text="Vérif Requirements", command=verif_requirements)
btn_requirements.grid(column=0, row=1, padx=10, pady=10)

btn_bypass = ttk.Button(frame, text="Bypass", command=bypass_verif)
btn_bypass.grid(column=0, row=4, padx=1, pady=1)

# Labels de statut
loading_label = ttk.Label(frame, text="⏳ Vérification en cours...", foreground="blue")
valid_label = ttk.Label(frame, text="✅ Chargement validé", foreground="green")

# Barre de progression (indéterminée)
progressbar = ttk.Progressbar(frame, mode="indeterminate", length=250)

oWindows.mainloop()
