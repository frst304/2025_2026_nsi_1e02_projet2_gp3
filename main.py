from import_datas import importer_donnees_covid19
from tkinter_config import creer_fenetre


def main():
    donnees = importer_donnees_covid19()
    fenetre = creer_fenetre()
    fenetre.mainloop()


if __name__ == "__main__":
    main()