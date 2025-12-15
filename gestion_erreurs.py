import tkinter as tk
from tkinter import messagebox
from tkinter_config import creer_fenetre


def afficher_message_erreur(erreur):
    fenetre = creer_fenetre()
    fenetre.withdraw()
    messagebox.showerror("Erreur", f"Erreur de chargement :\n{str(erreur)}")
    fenetre.destroy()

