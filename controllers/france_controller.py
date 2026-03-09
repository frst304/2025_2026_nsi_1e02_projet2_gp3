# Import pour les fenêtres de dialogue Tkinter
from tkinter import messagebox

# Import pandas pour la manipulation des données
import pandas as pd

# Import des fonctions pour détecter les colonnes dates
from models.region_service import DATE_COL_CANDIDATES, first_existing_column

# Liste des indicateurs nationaux disponibles : (Nom affiché, nom de colonne)
INDICATEURS_NATIONAUX = [
    ("Hospitalisations (nouvelles)", "incid_hosp"),
    ("Reanimations (nouvelles)", "incid_rea"),
    ("Deces hopital (nouveaux)", "incid_dchosp"),
    ("Hospitalises (actuels)", "hosp"),
    ("Reanimations (actuels)", "rea"),
    ("Deces hopital (cumul)", "dchosp"),
]

# Contrôleur pour la vue France (graphique national)
class FranceController:

    # Constructeur
    def __init__(self, donnees, view):
        self.donnees = donnees
        self.view = view

        # Détection automatique de la colonne date
        self.date_col = first_existing_column(donnees, DATE_COL_CANDIDATES)

        # Filtrage des indicateurs disponibles selon les colonnes présentes
        self.indicateurs_disponibles = [
            (label, col)
            for label, col in INDICATEURS_NATIONAUX
            if col in donnees.columns
        ]
        self.indicateur_labels = [label for label, _ in self.indicateurs_disponibles]

        # Remplir la vue avec les indicateurs et les dates
        self._fill_view()

        # Définir le callback lorsque l'utilisateur change la sélection
        self.view.set_on_selection_change(self.actualiser_graphique)

        # Afficher un message initial sur le graphique
        self.view.clear_plot("Selectionnez un indicateur et un intervalle de dates.")

    # Récupère les dates disponibles dans les données
    def _dates_disponibles(self):
        if not self.date_col or self.date_col not in self.donnees.columns:
            return []
        dates = (
            self.donnees[self.date_col]
            .dropna()
            .astype(str)
            .sort_values()
            .unique()
            .tolist()
        )
        return dates

    # Remplit la vue avec les indicateurs et dates
    def _fill_view(self):
        self.view.set_indicateurs(self.indicateur_labels)
        dates = self._dates_disponibles()
        self.view.set_dates(dates)

    # Filtre les données selon la période sélectionnée par l'utilisateur
    def _filtrer_par_dates(self):
        if not self.date_col or self.date_col not in self.donnees.columns:
            return self.donnees

        date_debut = self.view.get_date_debut()
        date_fin = self.view.get_date_fin()

        if not date_debut and not date_fin:
            return self.donnees

        # Conversion de la colonne de dates en datetime
        series_dates = pd.to_datetime(
            self.donnees[self.date_col], errors="coerce"
        )

        # Masque booléen pour filtrer les lignes
        masque = pd.Series(True, index=self.donnees.index)

        if date_debut:
            debut_dt = pd.to_datetime(date_debut, errors="coerce")
            if pd.notna(debut_dt):
                masque &= series_dates >= debut_dt

        if date_fin:
            fin_dt = pd.to_datetime(date_fin, errors="coerce")
            if pd.notna(fin_dt):
                masque &= series_dates <= fin_dt

        return self.donnees[masque].copy()

    # Actualise le graphique selon la sélection de l'utilisateur
    def actualiser_graphique(self):
        indicateur_label = self.view.get_indicateur_label()
        if not indicateur_label:
            self.view.clear_plot("Selectionnez un indicateur.")
            return

        # Trouver la colonne correspondant à l'indicateur sélectionné
        indicateur_col = None
        for label, col in self.indicateurs_disponibles:
            if label == indicateur_label:
                indicateur_col = col
                break

        if not indicateur_col:
            self.view.clear_plot("Indicateur invalide.")
            return

        try:
            # Filtrage des données selon les dates sélectionnées
            donnees_filtrees = self._filtrer_par_dates()
            if self.date_col and self.date_col in donnees_filtrees.columns:
                donnees_travail = donnees_filtrees.copy()
                donnees_travail[self.date_col] = pd.to_datetime(
                    donnees_travail[self.date_col], errors="coerce"
                )
                donnees_travail = donnees_travail.dropna(subset=[self.date_col])

                # Agrégation des données par date
                evolution = (
                    donnees_travail.groupby(self.date_col)[indicateur_col]
                    .sum()
                    .sort_index()
                )
            else:
                self.view.clear_plot("Aucune colonne de date valide pour tracer.")
                return

            # Récupérer l'objet axes du graphique et le nettoyer
            ax = self.view.get_plot_axes()
            ax.clear()

            # Tracer l'évolution de l'indicateur pour la France
            ax.plot(evolution.index, evolution.values, label="France")
            ax.set_title(f"Evolution de {indicateur_label} en France")
            ax.set_xlabel("Date")
            ax.set_ylabel(indicateur_label)
            ax.grid(True)
            ax.legend()

            # Redessiner le graphique dans la vue
            self.view.redraw_plot()

        # Gestion d'erreur éventuelle
        except ValueError as exc:
            messagebox.showerror("Erreur", str(exc))