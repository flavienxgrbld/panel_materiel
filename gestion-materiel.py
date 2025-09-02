import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os

FICHIER = "materiel.json"

# Chargement et sauvegarde
def charger_materiel():
    if os.path.exists(FICHIER):
        with open(FICHIER, 'r') as f:
            return json.load(f)
    return []

def sauvegarder_materiel(liste):
    with open(FICHIER, 'w') as f:
        json.dump(liste, f, indent=4)

# Fonctions GUI
def rafraichir_liste():
    liste_materiel.delete(0, tk.END)
    for item in materiels:
        texte = f"{item['nom']} - {item['categorie']} - {item['quantite']} unités"
        liste_materiel.insert(tk.END, texte)

def ajouter_materiel():
    nom = entry_nom.get()
    categorie = entry_categorie.get()
    quantite = entry_quantite.get()

    if not nom or not categorie or not quantite.isdigit():
        messagebox.showwarning("Erreur", "Veuillez remplir tous les champs correctement.")
        return

    materiels.append({
        "nom": nom,
        "categorie": categorie,
        "quantite": int(quantite)
    })
    sauvegarder_materiel(materiels)
    rafraichir_liste()
    entry_nom.delete(0, tk.END)
    entry_categorie.delete(0, tk.END)
    entry_quantite.delete(0, tk.END)

def supprimer_materiel():
    selection = liste_materiel.curselection()
    if not selection:
        messagebox.showwarning("Erreur", "Aucun matériel sélectionné.")
        return
    index = selection[0]
    del materiels[index]
    sauvegarder_materiel(materiels)
    rafraichir_liste()

def rechercher_materiel():
    mot_cle = simpledialog.askstring("Recherche", "Entrez un mot-clé :")
    if mot_cle:
        resultats = [m for m in materiels if mot_cle.lower() in m['nom'].lower() or mot_cle.lower() in m['categorie'].lower()]
        liste_materiel.delete(0, tk.END)
        for item in resultats:
            texte = f"{item['nom']} - {item['categorie']} - {item['quantite']} unités"
            liste_materiel.insert(tk.END, texte)

# Initialisation
materiels = charger_materiel()

# Interface principale
fenetre = tk.Tk()
fenetre.title("Gestion de Matériel")

# Champs de saisie
tk.Label(fenetre, text="Nom:").grid(row=0, column=0)
entry_nom = tk.Entry(fenetre)
entry_nom.grid(row=0, column=1)

tk.Label(fenetre, text="Catégorie:").grid(row=1, column=0)
entry_categorie = tk.Entry(fenetre)
entry_categorie.grid(row=1, column=1)

tk.Label(fenetre, text="Quantité:").grid(row=2, column=0)
entry_quantite = tk.Entry(fenetre)
entry_quantite.grid(row=2, column=1)

# Boutons
btn_ajouter = tk.Button(fenetre, text="Ajouter", command=ajouter_materiel)
btn_ajouter.grid(row=3, column=0, columnspan=2, pady=5)

btn_supprimer = tk.Button(fenetre, text="Supprimer", command=supprimer_materiel)
btn_supprimer.grid(row=4, column=0, columnspan=2)

btn_rechercher = tk.Button(fenetre, text="Rechercher", command=rechercher_materiel)
btn_rechercher.grid(row=5, column=0, columnspan=2, pady=5)

# Liste
liste_materiel = tk.Listbox(fenetre, width=50)
liste_materiel.grid(row=6, column=0, columnspan=2, pady=10)

rafraichir_liste()
fenetre.mainloop()
