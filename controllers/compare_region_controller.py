# Import pour fenêtres de dialogue Tkinter
from tkinter import messagebox

# Import pandas pour la manipulation des données
import pandas as pd

# Import des fonctions utilitaires pour gérer les colonnes de dates et régions
from models.region_service import (
    DATE_COL_CANDIDATES,
    comparer_regions,   # Fonction pour comparer graphiquement plusieurs régions
    first_existing_column,
    strip_accents,      # Supprime les accents pour normaliser le texte
)

# Liste des indicateurs disponibles pour comparaison
INDICATEURS = [
    ("Hospitalisations (nouvelles)", "incid_hosp"),
    ("Reanimations (nouvelles)", "incid_rea"),
    ("Deces hopital (nouveaux)", "incid_dchosp"),
    ("Hospitalises (actuels)", "hosp"),
    ("Reanimations (actuels)", "rea"),
    ("Deces hopital (cumul)", "dchosp"),
]

# Contrôleur pour la vue de comparaison régionale
class CompareRegionController:

    # Constructeur
    def __init__(self, donnees, region_col, view):
        self.donnees = donnees           # DataFrame des données Covid
        self.region_col = region_col     # Nom de la colonne contenant les régions
        self.view = view                 # Vue associée à ce contrôleur

        # Détection automatique de la colonne date
        self.date_col = first_existing_column(donnees, DATE_COL_CANDIDATES)

        # Filtrer les indicateurs disponibles selon les colonnes présentes
        self.indicateurs_disponibles = [
            (label, col)
            for label, col in INDICATEURS
            if col in donnees.columns
        ]
        self.indicateur_labels = [label for label, _ in self.indicateurs_disponibles]

        # Remplir la vue avec régions, indicateurs et dates
        self._fill_view()

        # Définir le callback lorsque l'utilisateur change la sélection
        self.view.set_on_selection_change(self.actualiser_graphique)

        # Afficher un message initial sur le graphique
        self.view.clear_plot("Selectionnez deux regions et un indicateur.")

    # Récupère toutes les régions disponibles dans les données
    def _regions_disponibles(self):
        if not self.region_col:
            return []
        regions = (
            self.donnees[self.region_col]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )
        # Retourner les régions triées et sans accents
        return sorted(strip_accents(r) for r in regions)

    # Remplit la vue avec les régions, indicateurs et dates disponibles
    def _fill_view(self):
        regions = self._regions_disponibles()
        self.view.set_regions(regions)
        self.view.set_indicateurs(self.indicateur_labels)
        dates = self._dates_disponibles()
        self.view.set_dates(dates)

    # Récupère toutes les dates disponibles
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

    # Filtre les données selon l'intervalle de dates sélectionné par l'utilisateur
    def _filtrer_par_dates(self):
        """
        Renvoie un DataFrame filtre sur l'intervalle de dates choisi.
        Si aucune date n'est choisie ou si la colonne date est absente,
        on renvoie l'ensemble des donnees.
        """
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
        masque = pd.Series(True, index=self.donnees.index)

        if date_debut:
            debut_dt = pd.to_datetime(date_debut, errors="coerce")
            if pd.notna(debut_dt):
                masque &= series_dates >= debut_dt

        if date_fin:
            fin_dt = pd.to_datetime(date_fin, errors="coerce")
            if pd.notna(fin_dt):
                masque &= series_dates <= fin_dt

        # Retourner le DataFrame filtré
        return self.donnees[masque].copy()

    # Lancer la comparaison des deux régions sélectionnées
    def lancer_comparaison(self):
        if not self.region_col:
            messagebox.showerror(
                "Erreur",
                "Aucune colonne de region detectee dans les donnees.",
            )
            return

        region_1 = self.view.get_region_1()
        region_2 = self.view.get_region_2()
        if not region_1 or not region_2:
            messagebox.showwarning(
                "Saisie incomplete",
                "Veuillez choisir deux regions.",
            )
            return

        indicateur_label = self.view.get_indicateur_label()
        indicateur_col = None
        for label, col in self.indicateurs_disponibles:
            if label == indicateur_label:
                indicateur_col = col
                break
        if not indicateur_col:
            messagebox.showwarning(
                "Indicateur manquant",
                "Veuillez choisir un indicateur valide.",
            )
            return

        try:
            # Filtrer les données selon l'intervalle de dates
            donnees_filtrees = self._filtrer_par_dates()

            # Utiliser la fonction comparer_regions pour tracer le graphique
            comparer_regions(
                donnees_filtrees,
                [region_1, region_2],
                region_col=self.region_col,
                value_col=indicateur_col,
                value_label=indicateur_label,
                ax=self.view.get_plot_axes(),
                show=False,
            )
            # Redessiner le graphique
            self.view.redraw_plot()
        except ValueError as exc:
            messagebox.showerror("Erreur", str(exc))

    # Met à jour le graphique à chaque changement de sélection
    def actualiser_graphique(self):
        if not self.region_col:
            self.view.clear_plot("Aucune colonne de region detectee.")
            return

        region_1 = self.view.get_region_1()
        region_2 = self.view.get_region_2()
        indicateur_label = self.view.get_indicateur_label()

        if not region_1 or not region_2 or not indicateur_label:
            self.view.clear_plot("Selectionnez deux regions et un indicateur.")
            return

        # Identifier la colonne correspondant à l'indicateur
        indicateur_col = None
        for label, col in self.indicateurs_disponibles:
            if label == indicateur_label:
                indicateur_col = col
                break
        if not indicateur_col:
            self.view.clear_plot("Indicateur invalide.")
            return

        try:
            # Filtrer les données selon les dates sélectionnées
            donnees_filtrees = self._filtrer_par_dates()
            # Tracer les régions sélectionnées
            comparer_regions(
                donnees_filtrees,
                [region_1, region_2],
                region_col=self.region_col,
                value_col=indicateur_col,
                value_label=indicateur_label,
                ax=self.view.get_plot_axes(),
                show=False,
            )
            self.view.redraw_plot()
        except ValueError as exc:
            # Afficher l'erreur dans le graphique
            self.view.clear_plot(str(exc))