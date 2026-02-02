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


def first_existing_column(df, candidates):
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


def strip_accents(text):
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
    ax=None,
    show=True,
):
    if isinstance(regions, str):
        regions = [regions]

    if not regions:
        raise ValueError("La liste des regions a comparer est vide.")

    if region_col is None:
        region_col = first_existing_column(df, REGION_COL_CANDIDATES)
    if date_col is None:
        date_col = first_existing_column(df, DATE_COL_CANDIDATES)
    if value_col is None:
        value_col = first_existing_column(df, HOSP_COL_CANDIDATES)

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

    if ax is None:
        fig = plt.figure(figsize=(10, 5))
        ax = fig.add_subplot(111)
    else:
        fig = ax.figure
        ax.clear()

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
        label = strip_accents(region) if normalize_regions else str(region)
        ax.plot(evolution.index, evolution.values, label=label)
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
    ax.set_title(titre)
    ax.set_xlabel("Date")
    ax.set_ylabel(value_label or "Nouvelles hospitalisations")
    locator = mdates.AutoDateLocator(minticks=4, maxticks=10)
    ax.xaxis.set_major_locator(locator)
    ax.xaxis.set_major_formatter(mdates.ConciseDateFormatter(locator))
    fig.autofmt_xdate()
    ax.legend()
    ax.grid(True)
    fig.tight_layout()
    regions_titre = " vs ".join(
        strip_accents(r) if normalize_regions else str(r) for r in regions
    )
    fenetre_titre = (
        f"{value_label or 'Comparaison'} - {regions_titre}"
    )
    if show:
        try:
            fig.canvas.manager.set_window_title(fenetre_titre)
        except Exception:
            pass
        plt.show()

    if regions_absentes:
        print(
            "Regions absentes dans les donnees: "
            + ", ".join(map(str, regions_absentes))
        )
