# Import de la boîte de dialogue pour afficher des messages d'erreur
from tkinter import messagebox

# Import de la fonction qui permet d'importer les données COVID
from models.data_importer import importer_donnees_covid19

# Import des constantes et fonctions utiles pour détecter la colonne des régions
from models.region_service import REGION_COL_CANDIDATES, first_existing_column

# Import des différentes vues de l'interface graphique
from views.main_window import MainWindow
from views.home_view import HomeView
from views.compare_region_view import CompareRegionView
from views.france_view import FranceView
from views.france_map_view import FranceMapView

# Import des contrôleurs qui gèrent la logique entre données et interface
from controllers.home_controller import HomeController
from controllers.compare_region_controller import CompareRegionController
from controllers.france_controller import FranceController
from controllers.france_map_controller import FranceMapController


def main():
    # Importation des données COVID depuis le fichier de données
    donnees = importer_donnees_covid19()

    # Recherche de la première colonne existante correspondant à une région
    region_col = first_existing_column(donnees, REGION_COL_CANDIDATES)

    # Si aucune colonne de région n'est trouvée, afficher une erreur
    if not region_col:
        messagebox.showerror(
            "Erreur",
            "Aucune colonne de region detectee dans les donnees.",
        )

    # Création de la fenêtre principale de l'application
    main_window = MainWindow()

    # Récupération du conteneur principal où seront affichées les pages
    contenu = main_window.contenu

    # Création des différentes vues (pages) de l'application
    home_view = HomeView(contenu)
    compare_region_view = CompareRegionView(contenu)
    france_view = FranceView(contenu)
    france_map_view = FranceMapView(contenu)

    # Ajout des pages dans la fenêtre principale
    main_window.add_page(home_view)
    main_window.add_page(compare_region_view)
    main_window.add_page(france_view)
    main_window.add_page(france_map_view)

    # Création des contrôleurs qui relient les données aux vues
    home_controller = HomeController(donnees, home_view)

    compare_region_controller = CompareRegionController(
        donnees, region_col, compare_region_view
    )

    france_controller = FranceController(donnees, france_view)

    france_map_controller = FranceMapController(donnees, france_map_view)

    # Ajout d'un bouton de navigation vers la page d'accueil
    main_window.add_nav_button(
        "Home",
        lambda: main_window.show_page(home_view),
        width=12,
    )

    # Ajout d'un bouton pour accéder à la comparaison des régions
    main_window.add_nav_button(
        "Comparer par regions",
        lambda: main_window.show_page(compare_region_view),
        width=20,
    )

    # Ajout d'un bouton pour afficher les données de toute la France
    main_window.add_nav_button(
        "France entiere",
        lambda: main_window.show_page(france_view),
        width=15,
    )

    # Ajout d'un bouton pour afficher la carte des départements
    main_window.add_nav_button(
        "Carte departements",
        lambda: main_window.show_page(france_map_view),
        width=18,
    )

    # Affichage initial de la page d'accueil
    main_window.show_page(home_view)

    # Lancement de la boucle principale de l'interface graphique
    main_window.mainloop()


# Vérifie que le fichier est exécuté directement (et pas importé comme module)
if __name__ == "__main__":
    main()