# Import de la bibliothèque tkinter pour créer l'interface graphique
import tkinter as tk

# Import des widgets ttk (versions améliorées des widgets tkinter)
from tkinter import ttk


# Classe qui représente la vue de la page d'accueil
class HomeView:

    # Constructeur de la classe
    def __init__(self, parent, **kwargs):

        # Création du frame principal de la page
        # parent correspond au conteneur dans lequel la page sera affichée
        self.frame = tk.Frame(parent, bg="#f4f6f8", **kwargs)

        # Construction de l'interface graphique
        self._build_ui()

    # Méthode privée qui construit les éléments de l'interface
    def _build_ui(self):

        # Création du titre de la page
        self.titre = ttk.Label(
            self.frame,
            text="Accueil",          # Texte affiché
            style="Titre.TLabel",    # Style défini dans styles.py
        )

        # Placement du titre avec un espace vertical
        self.titre.pack(pady=30)

        # Création d'un frame pour regrouper les statistiques
        self.stats_frame = tk.Frame(self.frame, bg="#f4f6f8")

        # Placement du frame des statistiques
        self.stats_frame.pack(pady=10)

        # Label affichant le nombre d'hospitalisations
        self.label_hosp = ttk.Label(
            self.stats_frame,
            text="Hospitalisations (actuels): indisponible",  # Valeur par défaut
            style="Stats.TLabel",
        )

        # Placement du label
        self.label_hosp.pack(pady=5)

        # Label affichant le nombre total de décès à l'hôpital
        self.label_deces = ttk.Label(
            self.stats_frame,
            text="Deces hopital (cumul): indisponible",  # Valeur par défaut
            style="Stats.TLabel",
        )

        # Placement du label
        self.label_deces.pack(pady=5)

    # Méthode permettant de mettre à jour les statistiques affichées
    def set_stats(self, total_hosp=None, total_deces=None):

        # Si la valeur des hospitalisations est disponible
        if total_hosp is not None:

            # Mise à jour du texte avec le nombre formaté (espaces pour les milliers)
            self.label_hosp.config(
                text=f"Hospitalisations (actuels): {int(total_hosp):,}".replace(",", " ")
            )

        else:
            # Si aucune donnée n'est disponible
            self.label_hosp.config(text="Hospitalisations (actuels): indisponible")

        # Si la valeur des décès est disponible
        if total_deces is not None:

            # Mise à jour du texte avec le nombre formaté
            self.label_deces.config(
                text=f"Deces hopital (cumul): {int(total_deces):,}".replace(",", " ")
            )

        else:
            # Si aucune donnée n'est disponible
            self.label_deces.config(text="Deces hopital (cumul): indisponible")