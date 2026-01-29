import unicodedata

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd


REGION_COL_CANDIDATES = [
    "region",
    "nom_reg",
    "lib_reg",
    "libelle_region",
    "region_name",
    "reg",
    "code_region",
]
DATE_COL_CANDIDATES = ["date", "jour"]
HOSP_COL_CANDIDATES = [
    "nouvelles_hospitalisations",
    "incid_hosp",
    "incid_hospitalisations",
    "incid_hospi",
]


def _first_existing_column(df, candidates):
    for col in candidates:
        if col in df.columns:
            return col
    return None


def _normalize_text(text):
    if text is None:
        return ""
    normalized = unicodedata.normalize("NFD", str(text))
    return "".join(
        char for char in normalized if unicodedata.category(char) != "Mn"
    ).strip().lower()


def _strip_accents(text):
    normalized = unicodedata.normalize("NFD", str(text))
    return "".join(
        char for char in normalized if unicodedata.category(char) != "Mn"
    ).strip()


def comparer_regions(
    df,
    regions,
    region_col=None,
    date_col=None,
    value_col=None,
    normalize_regions=True,
    value_label=None,
):
    """
    regions : liste de regions a comparer
    exemple : ["Ile-de-France", "Auvergne-Rhone-Alpes"]
    """
    if isinstance(regions, str):
        regions = [regions]

    if not regions:
        raise ValueError("La liste des regions a comparer est vide.")

    if region_col is None:
        region_col = _first_existing_column(df, REGION_COL_CANDIDATES)
    if date_col is None:
        date_col = _first_existing_column(df, DATE_COL_CANDIDATES)
    if value_col is None:
        value_col = _first_existing_column(df, HOSP_COL_CANDIDATES)

    missing = []
    if region_col is None:
        missing.append("region")
    if date_col is None:
        missing.append("date")
    if value_col is None:
        missing.append("nouvelles hospitalisations")
    if missing:
        raise ValueError(
            "Colonnes manquantes pour la comparaison: "
            + ", ".join(missing)
            + ". Colonnes disponibles: "
            + ", ".join(df.columns)
        )

    fig = plt.figure(figsize=(10, 5))

    regions_absentes = []
    traces = 0
    if normalize_regions:
        regions_key = df[region_col].astype(str).map(_normalize_text)
    for region in regions:
        if normalize_regions:
            region_key = _normalize_text(region)
            df_region = df[regions_key == region_key]
        else:
            df_region = df[df[region_col] == region]
        if df_region.empty:
            regions_absentes.append(region)
            continue

        evolution = df_region.groupby(date_col)[value_col].sum().sort_index()
        evolution.index = pd.to_datetime(evolution.index, errors="coerce")
        evolution = evolution[~evolution.index.isna()].sort_index()
        label = _strip_accents(region) if normalize_regions else str(region)
        plt.plot(evolution.index, evolution.values, label=label)
        traces += 1

    if traces == 0:
        raise ValueError(
            "Aucune region trouvee dans les donnees. "
            "Regions demandees: "
            + ", ".join(map(str, regions))
        )

    if value_label:
        titre = f"Comparaison des {value_label} par region"
    else:
        titre = "Comparaison des nouvelles hospitalisations Covid par region"
    plt.title(titre)
    plt.xlabel("Date")
    plt.ylabel(value_label or "Nouvelles hospitalisations")
    ax = plt.gca()
    locator = mdates.AutoDateLocator(minticks=4, maxticks=10)
    ax.xaxis.set_major_locator(locator)
    ax.xaxis.set_major_formatter(mdates.ConciseDateFormatter(locator))
    fig.autofmt_xdate()
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    regions_titre = " vs ".join(
        _strip_accents(r) if normalize_regions else str(r) for r in regions
    )
    fenetre_titre = (
        f"{value_label or 'Comparaison'} - {regions_titre}"
    )
    try:
        fig.canvas.manager.set_window_title(fenetre_titre)
    except Exception:
        pass
    

    if regions_absentes:
        print(
            "Regions absentes dans les donnees: "
            + ", ".join(map(str, regions_absentes))
        )
