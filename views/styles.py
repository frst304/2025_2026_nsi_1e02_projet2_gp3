# Import de la bibliothèque tkinter pour créer l'interface graphique
import tkinter as tk

# Import des widgets modernes de tkinter (ttk)
from tkinter import ttk


# Fonction qui applique les styles graphiques à la fenêtre
def appliquer_styles(fenetre):

    # Création d'un objet Style pour personnaliser l'apparence des widgets ttk
    style = ttk.Style()

    # Tentative d'utilisation du thème "clam"
    # Si ce thème n'est pas disponible, on ignore l'erreur
    try:
        style.theme_use("clam")
    except tk.TclError:
        pass

    # Configuration du style des listes déroulantes (Combobox)
    style.configure(
        "TCombobox",
        padding=6,  # Ajoute un espace interne autour du texte
    )

    # Style pour les labels utilisés comme titres
    style.configure(
        "Titre.TLabel",
        font=("Segoe UI", 18, "bold"),  # Police grande et en gras
        background="#f4f6f8",  # Couleur de fond
        foreground="#1f2a44",  # Couleur du texte
    )

    # Style pour les labels contenant du texte normal
    style.configure(
        "Texte.TLabel",
        font=("Segoe UI", 11),  # Police standard
        background="#f4f6f8",
        foreground="#2d3b55",
    )

    # Style pour les labels affichant des statistiques
    style.configure(
        "Stats.TLabel",
        font=("Segoe UI", 12, "bold"),  # Texte légèrement plus grand et en gras
        background="#f4f6f8",
        foreground="#1f2a44",
    )

    # Style pour les boutons de navigation
    style.configure(
        "Nav.TButton",
        font=("Segoe UI", 10, "bold"),  # Police en gras
        padding=8,  # Espace interne du bouton
    )

    # Style pour les boutons d'action (ex: valider, comparer, etc.)
    style.configure(
        "Action.TButton",
        font=("Segoe UI", 11, "bold"),  # Police un peu plus grande
        padding=8,
    )