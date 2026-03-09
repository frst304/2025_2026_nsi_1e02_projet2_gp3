# Import pour les fenêtres de dialogue Tkinter
from tkinter import messagebox

# Import pour manipuler des fichiers temporaires et ouvrir un navigateur
import json
import tempfile
import webbrowser

# Import pour la manipulation de données
import pandas as pd
import requests

# Import des fonctions pour détecter les colonnes dates et régions
from models.region_service import DATE_COL_CANDIDATES, first_existing_column

# Liste des noms possibles pour la colonne des départements
DEP_COL_CANDIDATES = ["dep", "departement", "code_dep", "code_departement"]

# Liste des indicateurs disponibles pour les départements
# (Nom affiché, nom de colonne dans le DataFrame)
INDICATEURS_DEPARTEMENTAUX = [
    ("Hospitalisations (nouvelles)", "incid_hosp"),
    ("Reanimations (nouvelles)", "incid_rea"),
    ("Deces hopital (nouveaux)", "incid_dchosp"),
    ("Hospitalises (actuels)", "hosp"),
    ("Reanimations (actuels)", "rea"),
    ("Deces hopital (cumul)", "dchosp"),
]


# Contrôleur pour la carte de France par départements
class FranceMapController:

    # Constructeur
    def __init__(self, donnees, view):
        self.donnees = donnees
        self.view = view

        # Détection automatique des colonnes date et département
        self.date_col = first_existing_column(donnees, DATE_COL_CANDIDATES)
        self.dep_col = first_existing_column(donnees, DEP_COL_CANDIDATES)

        # Filtrage des indicateurs disponibles en fonction des colonnes présentes
        self.indicateurs_disponibles = [
            (label, col)
            for label, col in INDICATEURS_DEPARTEMENTAUX
            if col in donnees.columns
        ]
        self.indicateur_labels = [label for label, _ in self.indicateurs_disponibles]

        # Remplir la vue avec les indicateurs et dates
        self._fill_view()

        # Définir le callback pour le bouton "Générer la carte"
        self.view.set_on_generate(self.generer_carte)

    # Méthode interne pour récupérer les dates disponibles dans les données
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

    # Remplit la vue avec indicateurs et dates disponibles
    def _fill_view(self):
        self.view.set_indicateurs(self.indicateur_labels)
        dates = self._dates_disponibles()
        self.view.set_dates(dates)

    # Vérifie que folium est installé et le charge
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

    # Télécharge un GeoJSON contenant les départements de France
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

    # Méthode principale pour générer la carte interactive
    def generer_carte(self):

        # Vérification que la colonne département existe
        if not self.dep_col:
            messagebox.showerror(
                "Colonnes manquantes",
                "Aucune colonne de departement trouvee dans les donnees.",
            )
            return

        # Charger folium
        folium = self._charger_folium()
        if folium is None:
            return

        # Récupérer la date choisie dans la vue
        date_str = self.view.get_date()
        if not date_str and self.date_col and self.date_col in self.donnees.columns:
            # On prend la dernière date disponible
            dates = self._dates_disponibles()
            if dates:
                date_str = dates[-1]

        if not date_str:
            messagebox.showerror(
                "Date manquante",
                "Aucune date selectionnee et aucune date disponible.",
            )
            return

        # Récupérer l'indicateur choisi dans la vue
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

        # Filtrer les données pour la date choisie
        df = self.donnees.copy()
        if self.date_col and self.date_col in df.columns:
            df[self.date_col] = pd.to_datetime(df[self.date_col], errors="coerce")
            date_cible = pd.to_datetime(date_str, errors="coerce")
            df = df[df[self.date_col] == date_cible]

        if df.empty:
            messagebox.showerror(
                "Aucune donnee",
                "Aucune donnee disponible pour la date selectionnee.",
            )
            return

        # Agréger les valeurs par département
        df_dep = (
            df.groupby(self.dep_col)[indicateur_col]
            .sum()
            .reset_index()
            .rename(columns={indicateur_col: "valeur"})
        )

        # Télécharger le GeoJSON des départements
        geojson = self._telecharger_geojson_departements()
        if geojson is None:
            return

        # Création de la carte centrée sur la France
        m = folium.Map(location=[46.5, 2.0], zoom_start=5, tiles="cartodbpositron")

        # Ajout du choropleth (carte colorée par valeur)
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

        # Ajout des popups pour chaque département avec les valeurs
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

        # Ajouter le contrôle des calques
        m.add_child(folium.LayerControl())

        # Sauvegarder la carte dans un fichier temporaire et ouvrir dans le navigateur
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

        # Ouverture automatique dans le navigateur par défaut
        webbrowser.open(url)