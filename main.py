from import_datas import importer_donnees_covid19
from traitement_donnees import preparer_donnees_pour_graphique_deces
from graphique import afficher_graphique_dans_fenetre
from gestion_erreurs import afficher_message_erreur
from tkinter_config import creer_fenetre


def main():
    try:
        donnees_brutes = importer_donnees_covid19()
        donnees_preparees = preparer_donnees_pour_graphique_deces(donnees_brutes)
        
        fenetre = creer_fenetre()
        afficher_graphique_dans_fenetre(fenetre, donnees_preparees)
        
        fenetre.mainloop()
    except Exception as erreur:
        afficher_message_erreur(erreur)


if __name__ == "__main__":
    main()