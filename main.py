import tkinter as tk
from tkinter import ttk, messagebox
import requests
import pandas as pd
import io

def charger_donnees():
    try:
        url = "https://www.data.gouv.fr/fr/datasets/r/55e734e6-5b24-4b5e-a6b4-8c1155e035a0"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        df = pd.read_csv(io.StringIO(response.text), delimiter=';')
        
        prenom_col = df.columns[df.columns.str.contains('prenom', case=False)][0]
        nombre_col = df.columns[df.columns.str.contains('nombre', case=False)][0]
        
        df = df[[prenom_col, nombre_col]].copy()
        df.columns = ['prenom', 'nombre']
        df = df.dropna()
        df = df[df['nombre'] > 0]
        df = df.head(100).sort_values('nombre', ascending=False)
        
        return list(zip(df['prenom'], df['nombre'].astype(int)))
    except:
        messagebox.showwarning("Info", "Utilisation de données d'exemple")
        return [
            ("Emma", 4500), ("Lucas", 4200), ("Léa", 3800), ("Gabriel", 3700),
            ("Chloé", 3600), ("Louis", 3500), ("Manon", 3400), ("Hugo", 3300),
            ("Camille", 3200), ("Nathan", 3100), ("Sarah", 3000), ("Thomas", 2900),
            ("Inès", 2800), ("Jules", 2700), ("Léna", 2600), ("Noah", 2500),
            ("Anna", 2400), ("Liam", 2300), ("Mia", 2200), ("Ethan", 2100),
            ("Lola", 2000), ("Paul", 1900), ("Zoé", 1800), ("Raphaël", 1700),
            ("Mila", 1600), ("Arthur", 1500), ("Rose", 1400), ("Adam", 1300),
            ("Ambre", 1200), ("Noé", 1100), ("Julia", 1000), ("Maël", 950),
            ("Lina", 900), ("Gabin", 850), ("Louise", 800), ("Nolan", 750),
            ("Alice", 700), ("Léo", 650), ("Maya", 600), ("Eden", 550),
            ("Lilou", 500), ("Timéo", 480), ("Agathe", 460), ("Naël", 440),
            ("Élise", 420), ("Noam", 400), ("Louna", 380), ("Sacha", 360),
            ("Aya", 340), ("Ayden", 320), ("Lya", 300), ("Nino", 280),
            ("Eva", 260), ("Alessio", 240), ("Léonie", 220), ("Malo", 200),
        ]

def afficher_prenoms():
    for item in tree.get_children():
        tree.delete(item)
    
    status_label.config(text="Chargement...")
    root.update()
    
    prenoms = charger_donnees()
    
    for prenom, nombre in prenoms:
        tree.insert("", "end", values=(prenom, nombre))
    status_label.config(text=f"{len(prenoms)} prénoms")

root = tk.Tk()
root.title("Prénoms - data.gouv.fr")
root.geometry("400x500")

btn = tk.Button(root, text="Charger les prénoms", command=afficher_prenoms)
btn.pack(pady=10)

tree = ttk.Treeview(root, columns=("Prénom", "Nombre"), show="headings", height=20)
tree.heading("Prénom", text="Prénom")
tree.heading("Nombre", text="Nombre")
tree.column("Prénom", width=200)
tree.column("Nombre", width=100)
tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

status_label = tk.Label(root, text="Cliquez pour charger", relief=tk.SUNKEN)
status_label.pack(fill=tk.X, side=tk.BOTTOM)

root.mainloop()
