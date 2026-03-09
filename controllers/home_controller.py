# Import de la bibliothèque pandas pour manipuler les données
import pandas as pd

# Import des constantes et fonctions utiles pour détecter la colonne des dates
from models.region_service import DATE_COL_CANDIDATES, first_existing_column


# Classe contrôleur pour la page d'accueil
class HomeController:

    # Constructeur du contrôleur
    def __init__(self, donnees, view):

        # Stockage des données (DataFrame)
        self.donnees = donnees

        # Stockage de la vue associée
        self.view = view

        # Mise à jour immédiate des statistiques affichées
        self.refresh()

    # Méthode permettant d'actualiser les statistiques de la page d'accueil
    def refresh(self):

        # Calcul du résumé national (hospitalisations et décès)
        total_hosp, total_deces = self._resume_national()

        # Envoi des statistiques à la vue pour affichage
        self.view.set_stats(total_hosp=total_hosp, total_deces=total_deces)

    # Méthode privée qui calcule les statistiques nationales
    def _resume_national(self):

        # Recherche automatique de la colonne contenant les dates
        date_col = first_existing_column(self.donnees, DATE_COL_CANDIDATES)

        # Si une colonne de date est trouvée
        if date_col:

            # Création d'une copie des données pour éviter de modifier l'original
            donnees_dates = self.donnees.copy()

            # Conversion de la colonne de dates en format datetime
            donnees_dates[date_col] = pd.to_datetime(
                donnees_dates[date_col], errors="coerce"
            )

            # Récupération de la date la plus récente
            date_max = donnees_dates[date_col].max()

            # Si la date maximale est valide
            if pd.notna(date_max):

                # Filtrage des données pour ne garder que la date la plus récente
                donnees_filtrees = donnees_dates[
                    donnees_dates[date_col] == date_max
                ]
            else:
                # Si la date n'est pas valide, on utilise toutes les données
                donnees_filtrees = self.donnees
        else:
            # Si aucune colonne de date n'existe, on utilise toutes les données
            donnees_filtrees = self.donnees

        # Calcul du total des hospitalisations si la colonne existe
        total_hosp = (
            donnees_filtrees["hosp"].sum()
            if "hosp" in donnees_filtrees.columns
            else None
        )

        # Calcul du total des décès à l'hôpital si la colonne existe
        total_deces = (
            donnees_filtrees["dchosp"].sum()
            if "dchosp" in donnees_filtrees.columns
            else None
        )

        # Retourne les deux statistiques
        return total_hosp, total_deces