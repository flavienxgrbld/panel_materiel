import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import json
import os

FICHIER_JSON = "commandes.json"
STATUTS = ["Nouveau", "En cours", "Livré", "Annulé"]

def charger_commandes():
    if os.path.isfile(FICHIER_JSON):
        with open(FICHIER_JSON, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def sauvegarder_commandes():
    with open(FICHIER_JSON, "w", encoding="utf-8") as f:
        json.dump(commandes, f, indent=4, ensure_ascii=False)

def ajouter_produit():
    produit = entry_produit.get()
    quantite = entry_quantite.get()
    if produit and quantite:
        produits_commande.append({"Produit": produit, "Quantité": quantite})
        afficher_produits_commande()
        entry_produit.delete(0, tk.END)
        entry_quantite.delete(0, tk.END)
    else:
        messagebox.showwarning("Champs manquants", "Veuillez remplir le produit et la quantité.")

def afficher_produits_commande():
    listbox_produits.delete(0, tk.END)
    for prod in produits_commande:
        listbox_produits.insert(tk.END, f"{prod['Produit']} (x{prod['Quantité']})")

def ajouter_commande():
    client = entry_client.get()
    date_commande = entry_date.get()
    statut = combo_statut.get()
    if all([client, date_commande, statut]) and produits_commande:
        commandes.append({
            "Client": client,
            "Produits": produits_commande.copy(),
            "Date": date_commande,
            "Statut": statut
        })
        sauvegarder_commandes()
        afficher_commandes()
        afficher_clients()  # <-- Ajout ici
        entry_client.delete(0, tk.END)
        entry_date.delete(0, tk.END)
        combo_statut.set("")
        produits_commande.clear()
        afficher_produits_commande()
    else:
        messagebox.showwarning("Champs manquants", "Veuillez remplir tous les champs et ajouter au moins un produit.")

def afficher_commandes(liste=None):
    for i in tree.get_children():
        tree.delete(i)
    for idx, cmd in enumerate(liste if liste is not None else commandes):
        produits_str = ", ".join([f"{p['Produit']} (x{p['Quantité']})" for p in cmd["Produits"]])
        tree.insert("", "end", iid=idx, values=(cmd["Client"], produits_str, cmd["Date"], cmd["Statut"]))

def supprimer_commande():
    selected = tree.selection()
    if selected:
        idx = int(selected[0])
        commandes.pop(idx)
        sauvegarder_commandes()
        afficher_commandes()
        afficher_clients()  # <-- Ajout ici
    else:
        messagebox.showwarning("Sélection", "Veuillez sélectionner une commande à supprimer.")

def clear_commandes():
    if messagebox.askyesno("Confirmation", "Vider toutes les commandes ?"):
        commandes.clear()
        sauvegarder_commandes()
        afficher_commandes()
        afficher_clients()  # <-- Ajout ici

index_modif = None  # Ajoute cette ligne en haut du fichier

def modifier_commande():
    global index_modif
    selected = tree.selection()
    if selected:
        idx_affiche = int(selected[0])
        # Trouve la commande sélectionnée dans la liste affichée
        values = tree.item(selected, "values")
        # Recherche l'index réel dans la liste commandes
        for i, cmd in enumerate(commandes):
            produits_str = ", ".join([f"{p['Produit']} (x{p['Quantité']})" for p in cmd["Produits"]])
            if (cmd["Client"], produits_str, cmd["Date"], cmd["Statut"]) == values:
                index_modif = i
                break
        cmd = commandes[index_modif]
        entry_client.delete(0, tk.END)
        entry_client.insert(0, cmd["Client"])
        entry_date.delete(0, tk.END)
        entry_date.insert(0, cmd["Date"])
        combo_statut.set(cmd["Statut"])
        produits_commande.clear()
        for prod in cmd["Produits"]:
            produits_commande.append(prod.copy())
        afficher_produits_commande()
        btn_ajouter.config(text="Enregistrer", command=enregistrer_modif)
    else:
        messagebox.showwarning("Sélection", "Veuillez sélectionner une commande à modifier.")

def enregistrer_modif():
    global index_modif
    client = entry_client.get()
    date_commande = entry_date.get()
    statut = combo_statut.get()
    if all([client, date_commande, statut]) and produits_commande and index_modif is not None:
        commandes[index_modif] = {
            "Client": client,
            "Produits": produits_commande.copy(),
            "Date": date_commande,
            "Statut": statut
        }
        sauvegarder_commandes()
        afficher_commandes()
        afficher_clients()  # <-- Ajout ici
        entry_client.delete(0, tk.END)
        entry_date.delete(0, tk.END)
        combo_statut.set("")
        produits_commande.clear()
        afficher_produits_commande()
        btn_ajouter.config(text="Ajouter", command=ajouter_commande)
        index_modif = None
    else:
        messagebox.showwarning("Champs manquants", "Veuillez remplir tous les champs et ajouter au moins un produit.")

def rechercher_commandes():
    mot_cle = entry_recherche.get().lower()
    resultats = []
    for cmd in commandes:
        if mot_cle in cmd["Client"].lower() or any(mot_cle in p["Produit"].lower() for p in cmd["Produits"]):
            resultats.append(cmd)
    afficher_commandes(resultats)

def get_clients():
    return sorted(set(cmd["Client"] for cmd in commandes))

def afficher_clients():
    listbox_clients.delete(0, tk.END)
    for client in get_clients():
        listbox_clients.insert(tk.END, client)

def filtrer_par_client(event):
    selection = listbox_clients.curselection()
    if selection:
        client = listbox_clients.get(selection[0])
        resultats = [cmd for cmd in commandes if cmd["Client"] == client]
        afficher_commandes(resultats)

commandes = charger_commandes()
produits_commande = []

root = tk.Tk()
root.title("Gestion de Commandes")
root.geometry("1200x800")
root.resizable(False, False)

frame_left = ttk.Frame(root, padding=20)
frame_left.place(relx=0.0, rely=0.0, relheight=1.0, relwidth=0.3)

frame_right = ttk.Frame(root, padding=20)
frame_right.place(relx=0.3, rely=0.0, relheight=1.0, relwidth=0.7)

# Liste des clients à gauche
ttk.Label(frame_left, text="Clients:").pack(anchor="nw")
listbox_clients = tk.Listbox(frame_left, height=25, width=25)
listbox_clients.pack(fill="both", expand=True)
listbox_clients.bind("<<ListboxSelect>>", filtrer_par_client)

# Formulaire et tableau dans frame_right
ttk.Label(frame_right, text="Client:").grid(row=0, column=0, sticky="w")
entry_client = ttk.Entry(frame_right)
entry_client.grid(row=0, column=1, pady=5)

ttk.Label(frame_right, text="Produit:").grid(row=1, column=0, sticky="w")
entry_produit = ttk.Entry(frame_right)
entry_produit.grid(row=1, column=1, pady=5)

ttk.Label(frame_right, text="Quantité:").grid(row=2, column=0, sticky="w")
entry_quantite = ttk.Entry(frame_right)
entry_quantite.grid(row=2, column=1, pady=5)

btn_ajouter_produit = ttk.Button(frame_right, text="Ajouter produit à la commande", command=ajouter_produit)
btn_ajouter_produit.grid(row=3, column=0, columnspan=2, pady=5)

ttk.Label(frame_right, text="Produits ajoutés:").grid(row=4, column=0, sticky="w")
listbox_produits = tk.Listbox(frame_right, height=4, width=40)
listbox_produits.grid(row=4, column=1, pady=5)

ttk.Label(frame_right, text="Date (YYYY-MM-DD):").grid(row=5, column=0, sticky="w")
entry_date = ttk.Entry(frame_right)
entry_date.grid(row=5, column=1, pady=5)
entry_date.insert(0, datetime.now().strftime("%Y-%m-%d"))

ttk.Label(frame_right, text="Statut:").grid(row=6, column=0, sticky="w")
combo_statut = ttk.Combobox(frame_right, values=STATUTS, state="readonly")
combo_statut.grid(row=6, column=1, pady=5)

btn_ajouter = ttk.Button(frame_right, text="Ajouter", command=ajouter_commande)
btn_ajouter.grid(row=7, column=0, columnspan=2, pady=10)

btn_modifier = ttk.Button(frame_right, text="Modifier", command=modifier_commande)
btn_modifier.grid(row=8, column=0, columnspan=2, pady=5)

btn_supprimer = ttk.Button(frame_right, text="Supprimer", command=supprimer_commande)
btn_supprimer.grid(row=9, column=0, columnspan=2, pady=5)

btn_clear = ttk.Button(frame_right, text="Vider les commandes", command=clear_commandes)
btn_clear.grid(row=10, column=0, columnspan=2, pady=5)

ttk.Label(frame_right, text="Recherche:").grid(row=11, column=0, sticky="w")
entry_recherche = ttk.Entry(frame_right)
entry_recherche.grid(row=11, column=1, pady=5)
btn_recherche = ttk.Button(frame_right, text="Rechercher", command=rechercher_commandes)
btn_recherche.grid(row=12, column=0, columnspan=2, pady=5)

tree = ttk.Treeview(
    frame_right,
    columns=("Client", "Produits", "Date", "Statut"),
    show="headings",
    height=8
)
for col in ("Client", "Produits", "Date", "Statut"):
    tree.heading(col, text=col)
    tree.column(col, width=180)
tree.grid(row=13, column=0, columnspan=2, pady=10)

afficher_commandes()
afficher_clients()

root.mainloop()