import pandas as pd


def verifier_colonnes_necessaires(dataframe, colonnes_requises):
    colonnes_manquantes = [col for col in colonnes_requises if col not in dataframe.columns]
    if colonnes_manquantes:
        raise KeyError(
            f"Colonnes manquantes : {colonnes_manquantes}. "
            f"Colonnes disponibles : {list(dataframe.columns)}"
        )


def convertir_colonne_date_en_datetime(dataframe, nom_colonne_date):
    dataframe[nom_colonne_date] = pd.to_datetime(dataframe[nom_colonne_date], errors='coerce')
    return dataframe


def filtrer_donnees_valides(dataframe, colonnes_requises):
    dataframe_filtre = dataframe.dropna(subset=colonnes_requises)
    return dataframe_filtre


def trier_donnees_par_date(dataframe, nom_colonne_date):
    dataframe_trie = dataframe.sort_values(nom_colonne_date)
    return dataframe_trie


def preparer_donnees_pour_graphique_deces(dataframe):
    dataframe_copie = dataframe.copy()
    
    nom_colonne_date = 'date'
    nom_colonne_deces = 'dc_tot'
    colonnes_requises = [nom_colonne_date, nom_colonne_deces]
    
    verifier_colonnes_necessaires(dataframe_copie, colonnes_requises)
    convertir_colonne_date_en_datetime(dataframe_copie, nom_colonne_date)
    dataframe_copie = filtrer_donnees_valides(dataframe_copie, colonnes_requises)
    dataframe_copie = trier_donnees_par_date(dataframe_copie, nom_colonne_date)
    
    if len(dataframe_copie) == 0:
        raise ValueError("Aucune donnée valide après le traitement")
    
    return dataframe_copie

