from tkinter import messagebox

import json
import tempfile
import webbrowser

import pandas as pd
import requests

from models.region_service import DATE_COL_CANDIDATES, first_existing_column


DEP_COL_CANDIDATES = ["dep", "departement", "code_dep", "code_departement"]

INDICATEURS_DEPARTEMENTAUX = [
    ("Hospitalisations (nouvelles)", "incid_hosp"),
    ("Reanimations (nouvelles)", "incid_rea"),
    ("Deces hopital (nouveaux)", "incid_dchosp"),
    ("Hospitalises (actuels)", "hosp"),
    ("Reanimations (actuels)", "rea"),
    ("Deces hopital (cumul)", "dchosp"),
]


class FranceMapController:

    def __init__(self, donnees, view):
        self.donnees = donnees
        self.view = view

        self.date_col = first_existing_column(donnees, DATE_COL_CANDIDATES)
        self.dep_col = first_existing_column(donnees, DEP_COL_CANDIDATES)

        self.indicateurs_disponibles = [
            (label, col)
            for label, col in INDICATEURS_DEPARTEMENTAUX
            if col in donnees.columns
        ]
        self.indicateur_labels = [label for label, _ in self.indicateurs_disponibles]

        self._fill_view()
        self.view.set_on_generate(self.generer_carte)

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

    def _fill_view(self):
        self.view.set_indicateurs(self.indicateur_labels)
        dates = self._dates_disponibles()
        self.view.set_dates(dates)

    def _charger_folium(self):
        try:
            import folium  # type: ignore
        except ImportError:
            messagebox.showerror(
                "Dependance manquante",
                "Le module 'folium' est requis pour generer la carte.\n"
                "Installez-le avec: pip install folium",
            )
            return None
        return folium

    def _telecharger_geojson_departements(self):
        """
        Telecharge un GeoJSON des departements de France.
        """
        url_geojson = (
            "https://france-geojson.gregoiredavid.fr/"
            "repo/departements.geojson"
        )
        try:
            resp = requests.get(url_geojson, timeout=15)
            resp.raise_for_status()
            return resp.json()
        except Exception as exc:
            messagebox.showerror(
                "Erreur de telechargement",
                f"Impossible de telecharger la carte des departements.\n{exc}",
            )
            return None

    def generer_carte(self):
        if not self.dep_col:
            messagebox.showerror(
                "Colonnes manquantes",
                "Aucune colonne de departement trouvee dans les donnees.",
            )
            return

        folium = self._charger_folium()
        if folium is None:
            return

        date_debut = self.view.get_date_debut()
        date_fin = self.view.get_date_fin()
        if not date_debut or not date_fin:
            messagebox.showerror(
                "Date manquante",
                "Veuillez choisir une date de debut et une date de fin.",
            )
            return

        indicateur_label = self.view.get_indicateur_label()
        indicateur_col = None
        for label, col in self.indicateurs_disponibles:
            if label == indicateur_label:
                indicateur_col = col
                break

        if not indicateur_col:
            messagebox.showerror(
                "Indicateur invalide",
                "Veuillez choisir un indicateur valide.",
            )
            return

        # Filtrer les donnees pour la periode choisie
        df = self.donnees.copy()
        if self.date_col and self.date_col in df.columns:
            df[self.date_col] = pd.to_datetime(df[self.date_col], errors="coerce")
            debut_dt = pd.to_datetime(date_debut, errors="coerce")
            fin_dt = pd.to_datetime(date_fin, errors="coerce")
            if pd.isna(debut_dt) or pd.isna(fin_dt):
                messagebox.showerror(
                    "Dates invalides",
                    "Veuillez choisir des dates valides.",
                )
                return
            if fin_dt < debut_dt:
                messagebox.showerror(
                    "Intervalle invalide",
                    "La date de fin doit etre apres la date de debut.",
                )
                return
            df = df[(df[self.date_col] >= debut_dt) & (df[self.date_col] <= fin_dt)]

        if df.empty:
            messagebox.showerror(
                "Aucune donnee",
                "Aucune donnee disponible pour la periode selectionnee.",
            )
            return

        # Agregation par departement
        df_dep = (
            df.groupby(self.dep_col)[indicateur_col]
            .sum()
            .reset_index()
            .rename(columns={indicateur_col: "valeur"})
        )

        geojson = self._telecharger_geojson_departements()
        if geojson is None:
            return

        # Creation de la carte
        m = folium.Map(location=[46.5, 2.0], zoom_start=5, tiles="cartodbpositron")

        folium.Choropleth(
            geo_data=geojson,
            name="choropleth",
            data=df_dep,
            columns=[self.dep_col, "valeur"],
            key_on="feature.properties.code",
            fill_color="YlOrRd",
            fill_opacity=0.7,
            line_opacity=0.2,
            legend_name=f"{indicateur_label} par departement",
        ).add_to(m)

        # Popup avec valeur pour chaque departement
        dep_dict = {
            str(row[self.dep_col]): row["valeur"] for _, row in df_dep.iterrows()
        }
        for feature in geojson.get("features", []):
            code_dep = str(feature.get("properties", {}).get("code", ""))
            nom_dep = feature.get("properties", {}).get("nom", code_dep)
            valeur = dep_dict.get(code_dep)
            if valeur is not None:
                texte = f"{nom_dep} ({code_dep})<br>{indicateur_label}: {valeur:.0f}"
            else:
                texte = f"{nom_dep} ({code_dep})<br>Aucune donnee"
            folium.Popup(texte).add_to(
                folium.GeoJson(
                    feature,
                    style_function=lambda _f: {
                        "fillOpacity": 0,
                        "color": "transparent",
                    },
                )
            )

        m.add_child(folium.LayerControl())

        # Sauvegarde dans un fichier temporaire et ouverture dans le navigateur
        try:
            with tempfile.NamedTemporaryFile(
                suffix=".html", delete=False, mode="w", encoding="utf-8"
            ) as tmp:
                m.save(tmp.name)
                url = f"file://{tmp.name}"
        except Exception as exc:
            messagebox.showerror(
                "Erreur lors de la sauvegarde",
                f"Impossible d'enregistrer la carte.\n{exc}",
            )
            return

        webbrowser.open(url)

