from tkinter import messagebox

import pandas as pd

from models.region_service import (
    DATE_COL_CANDIDATES,
    comparer_regions,
    first_existing_column,
    strip_accents,
)


INDICATEURS = [
    ("Hospitalisations (nouvelles)", "incid_hosp"),
    ("Reanimations (nouvelles)", "incid_rea"),
    ("Deces hopital (nouveaux)", "incid_dchosp"),
    ("Hospitalises (actuels)", "hosp"),
    ("Reanimations (actuels)", "rea"),
    ("Deces hopital (cumul)", "dchosp"),
]


class CompareRegionController:

    def __init__(self, donnees, region_col, view):
        self.donnees = donnees
        self.region_col = region_col
        self.view = view

        self.date_col = first_existing_column(donnees, DATE_COL_CANDIDATES)

        self.indicateurs_disponibles = [
            (label, col)
            for label, col in INDICATEURS
            if col in donnees.columns
        ]
        self.indicateur_labels = [label for label, _ in self.indicateurs_disponibles]

        self._fill_view()
        self.view.set_on_selection_change(self.actualiser_graphique)
        self.view.clear_plot("Selectionnez deux regions et un indicateur.")

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
        return sorted(strip_accents(r) for r in regions)

    def _fill_view(self):
        regions = self._regions_disponibles()
        self.view.set_regions(regions)
        self.view.set_indicateurs(self.indicateur_labels)
        dates = self._dates_disponibles()
        self.view.set_dates(dates)

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

        return self.donnees[masque].copy()

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
            donnees_filtrees = self._filtrer_par_dates()
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
            messagebox.showerror("Erreur", str(exc))

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
        indicateur_col = None
        for label, col in self.indicateurs_disponibles:
            if label == indicateur_label:
                indicateur_col = col
                break
        if not indicateur_col:
            self.view.clear_plot("Indicateur invalide.")
            return
        try:
            donnees_filtrees = self._filtrer_par_dates()
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
            self.view.clear_plot(str(exc))
