from import_datas import importer_donnees_covid19
from tkinter_config import creer_fenetre
from compare_region import REGION_COL_CANDIDATES


def main():
    donnees = importer_donnees_covid19()
    region_col = next(
        (col for col in REGION_COL_CANDIDATES if col in donnees.columns),
        None,
    )
    fenetre = creer_fenetre(donnees, region_col)
    fenetre.mainloop()


if __name__ == "__main__":
    main()