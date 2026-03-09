# Import de la bibliothèque tkinter pour créer l'interface graphique
import tkinter as tk

# Import de la fonction qui applique les styles graphiques
from .styles import appliquer_styles


# Classe qui représente la fenêtre principale de l'application
class MainWindow:

    # Constructeur de la classe
    def __init__(self):

        # Création de la fenêtre principale
        self.fenetre = tk.Tk()

        # Titre affiché en haut de la fenêtre
        self.fenetre.title("Projet python")

        # Taille initiale de la fenêtre
        self.fenetre.geometry("1000x600")

        # Couleur de fond de la fenêtre
        self.fenetre.configure(bg="#f4f6f8")

        # Application des styles définis dans le fichier styles.py
        appliquer_styles(self.fenetre)

        # Création de la barre de navigation
        self._build_nav_bar()

        # Création du conteneur principal qui affichera les pages
        self.contenu = tk.Frame(self.fenetre, bg="#f4f6f8")

        # Le conteneur occupe tout l'espace disponible
        self.contenu.pack(fill="both", expand=True)

        # Configuration de la grille pour permettre aux pages de s'étendre
        self.contenu.grid_rowconfigure(0, weight=1)
        self.contenu.grid_columnconfigure(0, weight=1)

    # Méthode privée pour créer la barre de navigation
    def _build_nav_bar(self):

        # Création d'un frame qui servira de barre de navigation
        self.nav_bar = tk.Frame(self.fenetre, bg="#1f2a44")

        # La barre occupe toute la largeur de la fenêtre
        self.nav_bar.pack(fill="x")

    # Méthode pour ajouter un bouton dans la barre de navigation
    def add_nav_button(self, text, command, width=12):

        # Création du bouton
        btn = tk.Button(
            self.nav_bar,          # Le bouton est placé dans la barre de navigation
            text=text,             # Texte affiché sur le bouton
            command=command,       # Fonction exécutée lorsqu'on clique
            width=width,           # Largeur du bouton
            bg="#1f2a44",          # Couleur de fond
            fg="#ffffff",          # Couleur du texte
            activebackground="#2b3a5c",  # Couleur quand on clique
            activeforeground="#ffffff",  # Couleur du texte quand on clique
            relief="flat",         # Style visuel du bouton (sans bordure)
        )

        # Placement du bouton dans la barre de navigation
        btn.pack(side="left", padx=5, pady=5)

        # Retourne le bouton créé
        return btn

    # Méthode pour ajouter une page (vue) dans le conteneur principal
    def add_page(self, view):

        # Placement de la frame de la vue dans la grille
        view.frame.grid(row=0, column=0, sticky="nsew")

    # Méthode pour afficher une page spécifique
    def show_page(self, view):

        # Met la frame de la vue au premier plan
        view.frame.tkraise()

    # Méthode pour lancer la boucle principale de l'application tkinter
    def mainloop(self):

        # Démarrage de l'application graphique
        self.fenetre.mainloop()