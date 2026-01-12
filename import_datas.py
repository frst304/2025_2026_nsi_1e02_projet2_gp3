import pandas as pd
import requests
from io import StringIO


def importer_donnees_covid19():
    url_donnees_covid = "https://static.data.gouv.fr/resources/synthese-des-indicateurs-de-suivi-de-lepidemie-covid-19/20230630-155906/table-indicateurs-open-data-france-2023-06-30-17h59.csv"
    
    response = requests.get(url_donnees_covid, verify=True)
    response.raise_for_status()
    
    dataframe = pd.read_csv(StringIO(response.text), sep=",", low_memory=False)
    
    return dataframe