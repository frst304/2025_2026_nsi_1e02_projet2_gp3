from tkinter import messagebox

from models.region_service import (
    comparer_regions,
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

        self.indicateurs_disponibles = [
            (label, col)
            for label, col in INDICATEURS
            if col in donnees.columns
        ]
        self.indicateur_labels = [label for label, _ in self.indicateurs_disponibles]

        self._fill_view()
        self.view.set_on_compare_callback(self.lancer_comparaison)
        self.view.set_on_selection_change(self.actualiser_graphique)
        self.actualiser_graphique()

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
            comparer_regions(
                self.donnees,
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
            self.view.clear_plot("Selection incomplete.")
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
            comparer_regions(
                self.donnees,
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
