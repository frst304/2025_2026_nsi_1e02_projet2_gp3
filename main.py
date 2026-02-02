from tkinter import messagebox

from models.data_importer import importer_donnees_covid19
from models.region_service import REGION_COL_CANDIDATES, first_existing_column
from views.main_window import MainWindow
from views.home_view import HomeView
from views.compare_region_view import CompareRegionView
from views.france_view import FranceView
from controllers.home_controller import HomeController
from controllers.compare_region_controller import CompareRegionController
from controllers.france_controller import FranceController


def main():
    donnees = importer_donnees_covid19()
    region_col = first_existing_column(donnees, REGION_COL_CANDIDATES)

    if not region_col:
        messagebox.showerror(
            "Erreur",
            "Aucune colonne de region detectee dans les donnees.",
        )

    main_window = MainWindow()
    contenu = main_window.contenu

    home_view = HomeView(contenu)
    compare_region_view = CompareRegionView(contenu)
    france_view = FranceView(contenu)

    main_window.add_page(home_view)
    main_window.add_page(compare_region_view)
    main_window.add_page(france_view)

    home_controller = HomeController(donnees, home_view)
    compare_region_controller = CompareRegionController(
        donnees, region_col, compare_region_view
    )
    france_controller = FranceController(donnees, france_view)

    main_window.add_nav_button(
        "Home",
        lambda: main_window.show_page(home_view),
        width=12,
    )
    main_window.add_nav_button(
        "Comparer par regions",
        lambda: main_window.show_page(compare_region_view),
        width=20,
    )
    main_window.add_nav_button(
        "France entiere",
        lambda: main_window.show_page(france_view),
        width=15,
    )

    main_window.show_page(home_view)
    main_window.mainloop()


if __name__ == "__main__":
    main()
