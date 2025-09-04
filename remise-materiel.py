from tkinter import *
from tkinter import ttk, messagebox, Text, W, E, HORIZONTAL
import tkinter as tk
from fpdf import FPDF
from datetime import date
import os
from datetime import datetime
import qrcode
import mysql.connector
import json


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")


with open("param.json", "r", encoding="utf-8") as f:
    params = json.load(f)



def get_user_from_db(user_id):
    try:
        conn = mysql.connector.connect(
            host=params["host"],
            user=params["user"],
            password=params["password"],
            database=params["database"]
        )

        cursor = conn.cursor()
        cursor.execute("SELECT nom, prenom, lieu FROM utilisateurs WHERE id=%s", (user_id,))
        row = cursor.fetchone()
        conn.close()
        return row
    except Exception as e:
        messagebox.showerror("Erreur", f"Connexion MySQL échouée : {e}")
        return None

def submit_user():
    user_id = entry_id_utilisateur.get()
    if not user_id.isdigit():
        messagebox.showerror("Erreur", "Veuillez entrer un ID utilisateur valide (nombre).")
        return

    user = get_user_from_db(user_id)
    if user:
        nom, prenom, lieu = user
        entry_nom.delete(0, END)
        entry_prenom.delete(0, END)
        entry_lieu.delete(0, END)
        entry_nom.insert(0, nom)
        entry_prenom.insert(0, prenom)
        entry_lieu.insert(0, lieu)
    else:
        messagebox.showerror("Erreur", "Aucun utilisateur trouvé avec cet ID.")



class FicheRemisePDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 16)
        self.image(os.path.join(BASE_DIR, "logo.png"), 10, 8, 33)
        self.cell(0, 10, "MATERIEL", ln=1, align="R")
        self.set_font("Arial", "B", 11)
        self.cell(0, 10, "Fiche de remise", ln=1, align="R")
        self.ln(5)

    def add_info(self, nom, prenom, lieu, date_remise):
        self.set_font("Arial", "", 12)
        self.cell(0, 10, f"Nom collaborateur : {nom}", ln=1)
        self.cell(0, 10, f"Prénom collaborateur : {prenom}", ln=1)
        self.cell(0, 10, f"Lieu de travail : {lieu}", ln=1)
        self.cell(0, 10, f"Date : {date_remise}", ln=1)
        self.ln(5)

    def add_table(self, items):
        self.set_font("Arial", "B", 12)
        self.cell(30, 10, "Qté", 1)
        self.cell(80, 10, "Matériel", 1)
        self.cell(60, 10, "N° de suivi", 1)
        self.ln()

        self.set_font("Arial", "", 12)
        for item in items:
            self.cell(30, 10, str(item["qte"]), 1)
            self.cell(80, 10, item["materiel"], 1)
            self.cell(60, 10, item["suivi"], 1)
            self.ln()

    def add_footer_text(self):
        self.ln(5)
        texte = (
            "Nous mettons à votre disposition des outils nécessaires à l'exécution de vos missions.\n"
            "Pour rappel, ces outils de travail sont indispensables à l'exécution de vos missions dans la mesure et appartiennent à la société.\n"
            "Au vu de leur valeur et de l'importance qu'ils revêtent pour l'exécution de vos missions, vous devez donc impérativement en prendre soin.\n"
            "À défaut de respect de cette dernière, nous serons alors contraints d'envisager individuellement le prononcé de sanctions disciplinaires.\n"
            "En tout état de cause, il est interdit, pendant la durée du présent engagement, d'utiliser ce matériel à des fins personnelles ou à en faire un usage contraire à l'intérêt de la société.\n"
            "De même, vous vous engagez à restituer immédiatement et spontanément l'ensemble des éléments appartenant à la société susceptible d'être en sa possession au jour de la rupture du présent contrat, sur simple demande et sans qu'il soit besoin d'une mise en demeure préalable.\n"
            "Il est expressément rappelé qu'à défaut de restitution, la société se réserve le droit de faire application des dispositions de l'article L. 3251-2 du Code du travail et de procéder aux compensations correspondant à la valeur du matériel et outils de travail non restitués.\n"
            "Veuillez agréer, nos salutations distinguées.\n"
            "Signature + Lu et approuvé :"
        )
        self.set_font("Arial", "", 10)
        self.multi_cell(0, 8, texte)

def generate_pdf(nom, prenom, lieu, items):
    if not nom or not prenom or not lieu:
        messagebox.showerror("Erreur", "Veuillez remplir les informations du collaborateur (nom, prénom, lieu).")
        return
    if not items:
        messagebox.showerror("Erreur", "La liste des items est vide.")
        return




    date_remise = entry_date.get() if date_active.get() else date.today().strftime("%d/%m/%Y")


    pdf = FicheRemisePDF()
    pdf.add_page()
    pdf.add_info(nom, prenom, lieu, date_remise)
    pdf.add_table(items)
    pdf.add_footer_text()

    filename = f"fiche_remise_{prenom}_{nom}_{time}.pdf"
    filename_colis = f"fiche_colis_{prenom}_{nom}_{time}.pdf"
    pdf.output(filename)

    texte_colis = f"{nom} {prenom} \n {lieu}"
    fiche_colis = FPDF(orientation="L", unit="mm", format="A4")
    fiche_colis.add_page()
    fiche_colis.set_font("helvetica", style="B", size=90)
    fiche_colis.multi_cell(190, 40, texte_colis, align='C')
    fiche_colis.output(filename_colis)

    qr = qrcode.QRCode(
    version =1,
    box_size =10,
    border=6)

    data =f"nom : {nom} \nprenom : {prenom} \nlieu {lieu} \nitems : {items}" 
    qr.add_data(data)
    qr.make(fit=True)
    image = qr.make_image(fill_color="black", back_color= "white")
    name_qrcode = f"qrcode_{nom}_{prenom}.png"
    image.save(name_qrcode)
    
    messagebox.showinfo("Succès", f"✅ Génération: OK")


 

oWindows = tk.Tk()
oWindows.title("🖥️ Préparation PC")
oWindows.resizable(False, False)

style = ttk.Style(oWindows)
style.theme_use('clam')  

frame = ttk.Frame(oWindows, padding=20)
frame.grid()



ttk.Label(frame, text="ID Utilisateur:").grid(column=0, row=0, sticky=W, padx=(0, 10), pady=5)
entry_id_utilisateur = ttk.Entry(frame, width=10)
entry_id_utilisateur.grid(column=1, row=0, sticky=W, pady=5)

btn_submit = ttk.Button(frame, text="🔍 Rechercher", command=submit_user)
btn_submit.grid(column=2, row=0, sticky=W, padx=5)

def toggle_date_entry():
    if date_active.get():
        label_date.grid(column=0, row=5, sticky=W, padx=(0, 10), pady=5)
        entry_date.grid(column=1, row=5, sticky=W, pady=5)
        entry_date.delete(0, END)
        entry_date.insert(0, date.today().strftime("%d/%m/%Y"))  # Affiche date du jour
        entry_date.config(state="normal")
    else:
        entry_date.delete(0, END)
        entry_date.grid_remove()
        label_date.grid_remove()



items = []

def ajouter_item():
    qte = entry_quantite.get()
    materiel = entry_materiel.get()
    suivi = entry_suivi.get()

    if not qte.isdigit() or int(qte) < 1:
        messagebox.showerror("Erreur", "La quantité doit être un entier positif.")
        return
    if not materiel.strip():
        messagebox.showerror("Erreur", "Le champ matériel est vide.")
        return
    if not suivi.strip():
        messagebox.showerror("Erreur", "Le champ suivi est vide.")
        return

    item = {
        "qte": int(qte),
        "materiel": materiel.strip(),
        "suivi": suivi.strip()
    }
    items.append(item)
    afficher_items()

    entry_quantite.delete(0, END)
    entry_materiel.delete(0, END)
    entry_suivi.delete(0, END)

def afficher_items():
    text_items.delete('1.0', END)
    for i, item in enumerate(items, 1):
        text_items.insert(END, f"{i}. Qté: {item['qte']}, Matériel: {item['materiel']}, Suivi: {item['suivi']}\n")

def clear_items():
    items.clear()
    afficher_items()


ttk.Label(frame, text="Nom:").grid(column=0, row=1, sticky=W, padx=(0, 10), pady=5)
entry_nom = ttk.Entry(frame, width=30)
entry_nom.grid(column=1, row=1, sticky=W, pady=5)

btn_quit = ttk.Button(frame, text="❌ Quitter", command=oWindows.destroy)
btn_quit.grid(column=2, row=1, sticky=E, padx=(10, 0))

ttk.Label(frame, text="Prénom:").grid(column=0, row=2, sticky=W, padx=(0, 10), pady=5)
entry_prenom = ttk.Entry(frame, width=30)
entry_prenom.grid(column=1, row=2, sticky=W, pady=5)

ttk.Label(frame, text="Lieu:").grid(column=0, row=3, sticky=W, padx=(0, 10), pady=5)
entry_lieu = ttk.Entry(frame, width=30)
entry_lieu.grid(column=1, row=3, sticky=W, pady=5)

# ✅ Checkbox sous "Lieu"
date_active = BooleanVar()
check_date = ttk.Checkbutton(frame, text="Modifier la date", variable=date_active, command=toggle_date_entry)
check_date.grid(column=1, row=4, sticky=W, pady=(0, 5))

# ✅ Champ "Date" désactivé par défaut
# ✅ Créer les widgets "Date" mais NE PAS les afficher tout de suite
label_date = ttk.Label(frame, text="Date:")
entry_date = ttk.Entry(frame, width=30, state="normal")  # État modifié via la fonction


# ✅ Décalage de tous les éléments suivants d'une ligne (à partir de ligne 6)
ttk.Separator(frame, orient=HORIZONTAL).grid(column=0, row=6, columnspan=3, sticky="ew", pady=15)

ttk.Label(frame, text="Quantité:").grid(column=0, row=7, sticky=W, padx=(0, 10), pady=5)
entry_quantite = ttk.Entry(frame, width=30)
entry_quantite.grid(column=1, row=7, sticky=W, pady=5)

ttk.Label(frame, text="Matériel:").grid(column=0, row=8, sticky=W, padx=(0, 10), pady=5)
entry_materiel = ttk.Entry(frame, width=30)
entry_materiel.grid(column=1, row=8, sticky=W, pady=5)

ttk.Label(frame, text="Suivi (N° de série):").grid(column=0, row=9, sticky=W, padx=(0, 10), pady=5)
entry_suivi = ttk.Entry(frame, width=30)
entry_suivi.grid(column=1, row=9, sticky=W, pady=5)

btn_ajouter = ttk.Button(frame, text="➕ Ajouter item", command=ajouter_item)
btn_ajouter.grid(column=1, row=10, sticky=W, pady=(10, 5))

text_items = Text(frame, height=10, width=70, wrap='word', relief='solid', borderwidth=1)
text_items.grid(column=0, row=11, columnspan=3, pady=15)

btn_clear_items = ttk.Button(frame, text="🗑️ Vider les items", command=clear_items)
btn_clear_items.grid(column=2, row=12, sticky=E, pady=10)

btn_generate_pdf = ttk.Button(frame, text="📄 Générer PDF", command=lambda: generate_pdf(
    entry_nom.get(),
    entry_prenom.get(),
    entry_lieu.get(),
    items
))
btn_generate_pdf.grid(column=1, row=12, sticky=W, pady=10)
                                                                                                                                                                  
oWindows.mainloop()