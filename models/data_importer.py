# Import de la bibliothèque pandas pour manipuler les données
import pandas as pd

# Import du module requests pour récupérer des données depuis internet
import requests

# Import de StringIO pour traiter une chaîne de caractères comme un fichier
from io import StringIO


# Fonction permettant d'importer les données COVID depuis data.gouv.fr
def importer_donnees_covid19():

    # URL du fichier CSV contenant les indicateurs de suivi de l'épidémie
    url_donnees_covid = (
        "https://static.data.gouv.fr/resources/"
        "synthese-des-indicateurs-de-suivi-de-lepidemie-covid-19/"
        "20230630-155909/table-indicateurs-open-data-dep-2023-06-30-17h59.csv"
    )

    # Envoi d'une requête HTTP pour récupérer le fichier
    response = requests.get(url_donnees_covid, verify=True)

    # Vérifie si la requête a réussi (sinon une erreur est levée)
    response.raise_for_status()

    # Décodage du contenu reçu en UTF-8
    # errors="replace" permet d'éviter les erreurs si certains caractères sont invalides
    contenu = response.content.decode("utf-8", errors="replace")

    # Lecture du contenu CSV avec pandas
    dataframe = pd.read_csv(
        StringIO(contenu),  # transforme la chaîne en pseudo-fichier
        sep=",",            # séparateur des colonnes
        low_memory=False,   # évite certains avertissements de pandas
    )

    # Retourne le DataFrame contenant toutes les données
    return dataframe