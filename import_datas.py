import pandas as pd
import requests
from io import StringIO


def telecharger_fichier_csv_depuis_url(url):
    response = requests.get(url, verify=True)
    response.raise_for_status()
    return response


def lire_csv_depuis_reponse_http(reponse_http, separateur=","):
    dataframe = pd.read_csv(StringIO(reponse_http.text), sep=separateur, low_memory=False)
    return dataframe


def importer_donnees_covid19():
    url_donnees_covid = "https://static.data.gouv.fr/resources/synthese-des-indicateurs-de-suivi-de-lepidemie-covid-19/20230630-155906/table-indicateurs-open-data-france-2023-06-30-17h59.csv"
    
    reponse = telecharger_fichier_csv_depuis_url(url_donnees_covid)
    dataframe = lire_csv_depuis_reponse_http(reponse, separateur=",")
    
    return dataframe