import tkinter as tk
from tkinter import ttk, messagebox

materiels = []

def ajouter_materiel():
    nom = entry_nom.get()
    etat = combo_etat.get()
    depot = entry_depot.get()
    marque = entry_marque.get()
    proprietaire = entry_proprietaire.get()
    type_ = entry_type.get()
    sous_type = entry_sous_type.get()
    if all([nom, etat, depot, marque, proprietaire, type_, sous_type]):
        materiels.append({
            "Nom": nom,
            "État": etat,
            "Dépôt": depot,
            "Marque": marque,
            "Propriétaire": proprietaire,
            "Type": type_,
            "Sous-type": sous_type
        })
        afficher_materiels()
        entry_nom.delete(0, tk.END)
        combo_etat.set("")
        entry_depot.delete(0, tk.END)
        entry_marque.delete(0, tk.END)
        entry_proprietaire.delete(0, tk.END)
        entry_type.delete(0, tk.END)
        entry_sous_type.delete(0, tk.END)
    else:
        messagebox.showwarning("Champs manquants", "Veuillez remplir tous les champs.")

def afficher_materiels():
    for i in tree.get_children():
        tree.delete(i)
    for idx, mat in enumerate(materiels):
        tree.insert("", "end", iid=idx, values=(
            mat["Nom"], mat["État"], mat["Dépôt"], mat["Marque"],
            mat["Propriétaire"], mat["Type"], mat["Sous-type"]
        ))

def supprimer_materiel():
    selected = tree.selection()
    if selected:
        idx = int(selected[0])
        materiels.pop(idx)
        afficher_materiels()
    else:
        messagebox.showwarning("Sélection", "Veuillez sélectionner un matériel à supprimer.")

root = tk.Tk()
root.title("Gestion de Matériel Informatique")
root.geometry("900x400")
root.resizable(False, False)

frame = ttk.Frame(root, padding=10)
frame.pack(fill="both", expand=True)

ttk.Label(frame, text="Nom:").grid(row=0, column=0, sticky="w")
entry_nom = ttk.Entry(frame)
entry_nom.grid(row=0, column=1, pady=5)

ttk.Label(frame, text="État:").grid(row=0, column=2, sticky="w")
combo_etat = ttk.Combobox(frame, values=["Actif", "Inactif"], state="readonly")
combo_etat.grid(row=0, column=3, pady=5)

ttk.Label(frame, text="Dépôt:").grid(row=1, column=0, sticky="w")
entry_depot = ttk.Entry(frame)
entry_depot.grid(row=1, column=1, pady=5)

ttk.Label(frame, text="Marque:").grid(row=1, column=2, sticky="w")
entry_marque = ttk.Entry(frame)
entry_marque.grid(row=1, column=3, pady=5)

ttk.Label(frame, text="Propriétaire:").grid(row=2, column=0, sticky="w")
entry_proprietaire = ttk.Entry(frame)
entry_proprietaire.grid(row=2, column=1, pady=5)

ttk.Label(frame, text="Type:").grid(row=2, column=2, sticky="w")
entry_type = ttk.Entry(frame)
entry_type.grid(row=2, column=3, pady=5)

ttk.Label(frame, text="Sous-type:").grid(row=3, column=0, sticky="w")
entry_sous_type = ttk.Entry(frame)
entry_sous_type.grid(row=3, column=1, pady=5)

btn_ajouter = ttk.Button(frame, text="Ajouter", command=ajouter_materiel)
btn_ajouter.grid(row=3, column=2, columnspan=2, pady=10)

tree = ttk.Treeview(
    frame,
    columns=("Nom", "État", "Dépôt", "Marque", "Propriétaire", "Type", "Sous-type"),
    show="headings",
    height=10
)
for col in ("Nom", "État", "Dépôt", "Marque", "Propriétaire", "Type", "Sous-type"):
    tree.heading(col, text=col)
    tree.column(col, width=120)
tree.grid(row=4, column=0, columnspan=4, pady=10)

btn_supprimer = ttk.Button(frame, text="Supprimer", command=supprimer_materiel)
btn_supprimer.grid(row=5, column=0, columnspan=4, pady=5)

root.mainloop()