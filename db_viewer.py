import sqlite3
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import json
from store_database import StoreDB

db = StoreDB('stores.db')

root = tk.Tk()
root.title("Informations sur les Employés")

# Créez le menu déroulant pour sélectionner la table
table_label = tk.Label(root, text="Sélectionner une table :")
table_label.pack()
# Créez un style pour le menu déroulant
style = ttk.Style()
style.theme_use('clam')  # Choisissez un thème pour le menu déroulant, par exemple 'clam'



tables=StoreDB('stores.db').get_tables_list()
tables_list=[]
for each in tables:
    tables_list.append(each[0])
selected_table = tk.StringVar()
table_menu = ttk.Combobox(root, textvariable=selected_table, values=tables, style='TCombobox')
table_menu.pack()

# Bouton pour afficher les données de la table sélectionnée
def afficher_donnees():
    table_name = selected_table.get()
    column_names, data = db.get_table_data(table_name)
    if data:
        # Effacez les éléments existants dans le Treeview
        tree.delete(*tree.get_children())

        # Configurez les en-têtes du Treeview avec les noms des colonnes
        tree["columns"] = column_names
        for col in column_names:
            tree.column(col, anchor="center")
            tree.heading(col, text=col)

        # Ajoutez les données à afficher dans le Treeview
        for row in data:
            tree.insert("", "end", values=row)

afficher_button = tk.Button(root, text="Afficher", command=afficher_donnees)
afficher_button.pack()

tree = ttk.Treeview(root, columns=("ID", "Nom", "Prénom", "Date d'Entrée", "Jour de Repos", "Heures Semaine", "Rôle ID", "Magasin ID"), show="headings")
tree.pack(expand=True, fill=tk.BOTH)


# tree = ttk.Treeview(root, columns=("ID", "Nom", "Prénom", "Date d'Entrée", "Jour de Repos", "Heures Semaine", "Rôle ID", "Magasin ID"), show="headings")
# tree.heading("ID", text="ID")
# tree.heading("Nom", text="Nom")
# tree.heading("Prénom", text="Prénom")
# tree.heading("Date d'Entrée", text="Date d'Entrée")
# tree.heading("Jour de Repos", text="Jour de Repos")
# tree.heading("Heures Semaine", text="Heures Semaine")
# tree.heading("Rôle ID", text="Rôle ID")
# tree.heading("Magasin ID", text="Magasin ID")

# employes = db.get_employes()
# for employe in employes:
#     tree.insert("", "end", values=employe)

def importer_depuis_json():
    file_path = filedialog.askopenfilename(title="Sélectionner un fichier JSON")
    if file_path:
        db.import_depuis_json(file_path)
        # Mettez à jour l'affichage dans le Treeview
        employes = db.get_employes()
        tree.delete(*tree.get_children())  # Efface les éléments existants dans le Treeview
        for employe in employes:
            tree.insert("", "end", values=employe)

# tree.pack(expand=True, fill=tk.BOTH)
importer_button = tk.Button(root, text="Importer depuis JSON", command=importer_depuis_json)
importer_button.pack()

root.mainloop()
