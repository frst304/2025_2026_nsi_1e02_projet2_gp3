# Import du module permettant de gérer les accents et la normalisation des caractères
import unicodedata

# Import des outils matplotlib pour gérer les dates sur les graphiques
import matplotlib.dates as mdates

# Import de matplotlib pour créer des graphiques
import matplotlib.pyplot as plt

# Import de pandas pour manipuler les données (DataFrame)
import pandas as pd


# Liste des noms possibles pour la colonne contenant les régions
REGION_COL_CANDIDATES = [
    "region",
    "nom_reg",
    "lib_reg",
    "libelle_region",
    "region_name",
    "reg",
    "code_region",
]

# Liste des noms possibles pour la colonne contenant les dates
DATE_COL_CANDIDATES = ["date", "jour"]

# Liste des noms possibles pour la colonne contenant les hospitalisations
HOSP_COL_CANDIDATES = [
    "nouvelles_hospitalisations",
    "incid_hosp",
    "incid_hospitalisations",
    "incid_hospi",
]


# Fonction qui retourne la première colonne existante dans le DataFrame
# parmi une liste de noms possibles
def first_existing_column(df, candidates):
    for col in candidates:
        if col in df.columns:
            return col
    return None


# Fonction interne permettant de normaliser un texte
# (supprime les accents et met en minuscules)
def _normalize_text(text):
    if text is None:
        return ""

    # Transformation Unicode pour séparer les accents
    normalized = unicodedata.normalize("NFD", str(text))

    # Suppression des accents
    return "".join(
        char for char in normalized if unicodedata.category(char) != "Mn"
    ).strip().lower()


# Fonction qui supprime uniquement les accents d'un texte
def strip_accents(text):

    # Transformation Unicode
    normalized = unicodedata.normalize("NFD", str(text))

    # Suppression des caractères accentués
    return "".join(
        char for char in normalized if unicodedata.category(char) != "Mn"
    ).strip()


# Fonction principale permettant de comparer plusieurs régions sur un graphique
def comparer_regions(
    df,                      # DataFrame contenant les données
    regions,                 # liste des régions à comparer
    region_col=None,         # colonne des régions
    date_col=None,           # colonne des dates
    value_col=None,          # colonne des valeurs à comparer
    normalize_regions=True,  # normalisation des noms de régions
    value_label=None,        # nom de l'indicateur affiché
    ax=None,                 # axe matplotlib existant
    show=True,               # afficher le graphique
):

    # Si une seule région est fournie sous forme de texte,
    # on la transforme en liste
    if isinstance(regions, str):
        regions = [regions]

    # Vérification que la liste des régions n'est pas vide
    if not regions:
        raise ValueError("La liste des regions a comparer est vide.")

    # Détection automatique des colonnes si elles ne sont pas spécifiées
    if region_col is None:
        region_col = first_existing_column(df, REGION_COL_CANDIDATES)
    if date_col is None:
        date_col = first_existing_column(df, DATE_COL_CANDIDATES)
    if value_col is None:
        value_col = first_existing_column(df, HOSP_COL_CANDIDATES)

    # Vérification des colonnes manquantes
    missing = []
    if region_col is None:
        missing.append("region")
    if date_col is None:
        missing.append("date")
    if value_col is None:
        missing.append("nouvelles hospitalisations")

    # Si des colonnes sont manquantes on lève une erreur
    if missing:
        raise ValueError(
            "Colonnes manquantes pour la comparaison: "
            + ", ".join(missing)
            + ". Colonnes disponibles: "
            + ", ".join(df.columns)
        )

    # Création d'une figure matplotlib si aucun axe n'est fourni
    if ax is None:
        fig = plt.figure(figsize=(10, 5))
        ax = fig.add_subplot(111)
    else:
        fig = ax.figure
        ax.clear()

    # Liste des régions absentes dans les données
    regions_absentes = []

    # Compteur du nombre de courbes tracées
    traces = 0

    # Normalisation des noms de régions dans le DataFrame
    if normalize_regions:
        regions_key = df[region_col].astype(str).map(_normalize_text)

    # Boucle sur chaque région demandée
    for region in regions:

        # Filtrage des données selon la région
        if normalize_regions:
            region_key = _normalize_text(region)
            df_region = df[regions_key == region_key]
        else:
            df_region = df[df[region_col] == region]

        # Si aucune donnée trouvée pour la région
        if df_region.empty:
            regions_absentes.append(region)
            continue

        # Calcul de l'évolution dans le temps (somme par date)
        evolution = df_region.groupby(date_col)[value_col].sum().sort_index()

        # Conversion des dates en format datetime
        evolution.index = pd.to_datetime(evolution.index, errors="coerce")

        # Suppression des dates invalides
        evolution = evolution[~evolution.index.isna()].sort_index()

        # Nom de la courbe affichée dans la légende
        label = strip_accents(region) if normalize_regions else str(region)

        # Tracé de la courbe
        ax.plot(evolution.index, evolution.values, label=label)

        traces += 1

    # Si aucune région valide n'a été trouvée
    if traces == 0:
        raise ValueError(
            "Aucune region trouvee dans les donnees. "
            "Regions demandees: "
            + ", ".join(map(str, regions))
        )

    # Définition du titre du graphique
    if value_label:
        titre = f"Comparaison des {value_label} par region"
    else:
        titre = "Comparaison des nouvelles hospitalisations Covid par region"

    ax.set_title(titre)

    # Nom de l'axe X
    ax.set_xlabel("Date")

    # Nom de l'axe Y
    ax.set_ylabel(value_label or "Nouvelles hospitalisations")

    # Configuration automatique des dates sur l'axe X
    locator = mdates.AutoDateLocator(minticks=4, maxticks=10)
    ax.xaxis.set_major_locator(locator)
    ax.xaxis.set_major_formatter(mdates.ConciseDateFormatter(locator))

    # Ajustement automatique de l'affichage des dates
    fig.autofmt_xdate()

    # Affichage de la légende
    ax.legend()

    # Affichage de la grille
    ax.grid(True)

    # Ajustement automatique de la mise en page
    fig.tight_layout()

    # Création du titre de la fenêtre
    regions_titre = " vs ".join(
        strip_accents(r) if normalize_regions else str(r) for r in regions
    )

    fenetre_titre = (
        f"{value_label or 'Comparaison'} - {regions_titre}"
    )

    # Affichage du graphique si demandé
    if show:
        try:
            fig.canvas.manager.set_window_title(fenetre_titre)
        except Exception:
            pass

        plt.show()

    # Affiche les régions non trouvées dans les données
    if regions_absentes:
        print(
            "Regions absentes dans les donnees: "
            + ", ".join(map(str, regions_absentes))
        )