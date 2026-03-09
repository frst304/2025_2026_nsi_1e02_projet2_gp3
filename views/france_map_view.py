# Import de la bibliothèque tkinter pour créer l'interface graphique
import tkinter as tk

# Import des widgets ttk (versions améliorées des widgets tkinter)
from tkinter import ttk


# Classe représentant la vue qui permet d'afficher une carte de France par département
class FranceMapView:

    # Constructeur de la classe
    def __init__(self, parent, **kwargs):

        # Création du frame principal de la page
        self.frame = tk.Frame(parent, bg="#f4f6f8", **kwargs)

        # Construction de l'interface graphique
        self._build_ui()

    # Méthode privée qui construit les éléments de l'interface
    def _build_ui(self):

        # Création du titre de la page
        self.titre = ttk.Label(
            self.frame,
            text="Carte de France par departement",
            style="Titre.TLabel",
        )

        # Placement du titre avec un espace vertical
        self.titre.pack(pady=20)

        # Frame principal qui contiendra les éléments de la page
        self.content_frame = tk.Frame(self.frame, bg="#f4f6f8")

        # Le frame occupe tout l'espace disponible
        self.content_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Frame contenant les éléments de formulaire (sélections utilisateur)
        self.form_frame = tk.Frame(self.content_frame, bg="#f4f6f8")

        # Placement du formulaire en haut à gauche
        self.form_frame.pack(anchor="nw")

        # Label pour sélectionner l'indicateur
        ttk.Label(self.form_frame, text="Indicateur:", style="Texte.TLabel").pack(
            pady=(10, 5)
        )

        # Variable tkinter qui stocke l'indicateur sélectionné
        self.indicateur_var = tk.StringVar()

        # Liste déroulante permettant de choisir un indicateur
        self.liste_indicateur = ttk.Combobox(
            self.form_frame,
            textvariable=self.indicateur_var,
            values=[],           # Liste vide au départ
            state="readonly",    # L'utilisateur doit choisir dans la liste
            width=40,
        )
        self.liste_indicateur.pack()

        # Label pour choisir une date
        ttk.Label(self.form_frame, text="Date:", style="Texte.TLabel").pack(
            pady=(15, 5)
        )

        # Variable tkinter pour stocker la date sélectionnée
        self.date_var = tk.StringVar()

        # Liste déroulante pour choisir la date
        self.liste_date = ttk.Combobox(
            self.form_frame,
            textvariable=self.date_var,
            values=[],
            state="readonly",
            width=40,
        )
        self.liste_date.pack()

        # Bouton permettant de générer la carte interactive
        self.btn_generer = ttk.Button(
            self.form_frame,
            text="Generer la carte interactive",
        )

        # Placement du bouton avec un espace vertical
        self.btn_generer.pack(pady=20)

        # Label informatif indiquant où la carte sera affichée
        self.label_info = ttk.Label(
            self.frame,
            text="La carte sera ouverte dans votre navigateur par defaut.",
            style="Texte.TLabel",
        )

        # Placement du message d'information
        self.label_info.pack(pady=(0, 10))

    # Méthode permettant de définir la liste des indicateurs disponibles
    def set_indicateurs(self, indicateurs):

        # Remplit la liste déroulante avec les indicateurs
        self.liste_indicateur["values"] = indicateurs

        # Sélection automatique du premier indicateur si la liste n'est pas vide
        if indicateurs:
            self.indicateur_var.set(indicateurs[0])
        else:
            self.indicateur_var.set("")

    # Méthode permettant de définir la liste des dates disponibles
    def set_dates(self, dates):

        # Remplit la liste déroulante des dates
        self.liste_date["values"] = dates

        # Sélection automatique de la dernière date si la liste n'est pas vide
        if dates:
            self.date_var.set(dates[-1])
        else:
            self.date_var.set("")

    # Retourne l'indicateur sélectionné par l'utilisateur
    def get_indicateur_label(self):
        return self.indicateur_var.get().strip()

    # Retourne la date sélectionnée par l'utilisateur
    def get_date(self):
        return self.date_var.get().strip()

    # Méthode permettant d'associer une fonction au bouton "Generer la carte"
    def set_on_generate(self, callback):

        # Lorsque le bouton est cliqué, la fonction callback est exécutée
        self.btn_generer.config(command=callback)