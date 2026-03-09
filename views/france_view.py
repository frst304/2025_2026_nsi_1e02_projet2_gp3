# Import de la bibliothèque tkinter pour l'interface graphique
import tkinter as tk

# Import des widgets ttk (versions améliorées des widgets tkinter)
from tkinter import ttk

# Import du composant permettant d'intégrer un graphique matplotlib dans tkinter
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Import de l'objet Figure de matplotlib pour créer des graphiques
from matplotlib.figure import Figure


# Classe représentant la vue pour afficher les données de toute la France
class FranceView:

    # Constructeur de la classe
    def __init__(self, parent, **kwargs):

        # Création du frame principal de la page
        self.frame = tk.Frame(parent, bg="#f4f6f8", **kwargs)

        # Construction de l'interface graphique
        self._build_ui()

    # Méthode privée qui construit l'interface
    def _build_ui(self):

        # Création du titre de la page
        self.titre = ttk.Label(
            self.frame,
            text="France entiere",
            style="Titre.TLabel",
        )

        # Placement du titre
        self.titre.pack(pady=20)

        # Frame principal contenant les contrôles et le graphique
        self.content_frame = tk.Frame(self.frame, bg="#f4f6f8")

        # Le frame occupe tout l'espace disponible
        self.content_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Configuration de la grille
        self.content_frame.grid_columnconfigure(0, weight=0)
        self.content_frame.grid_columnconfigure(1, weight=1)
        self.content_frame.grid_rowconfigure(0, weight=1)

        # -------------------------
        # Panneau de gauche : choix de l'indicateur et des dates
        # -------------------------

        # Frame contenant les contrôles utilisateur
        self.form_frame = tk.Frame(self.content_frame, bg="#f4f6f8")

        # Placement dans la grille
        self.form_frame.grid(row=0, column=0, sticky="nw")

        # Label pour sélectionner l'indicateur
        ttk.Label(self.form_frame, text="Indicateur:", style="Texte.TLabel").pack(
            pady=(10, 5)
        )

        # Variable tkinter pour stocker l'indicateur sélectionné
        self.indicateur_var = tk.StringVar()

        # Liste déroulante des indicateurs
        self.liste_indicateur = ttk.Combobox(
            self.form_frame,
            textvariable=self.indicateur_var,
            values=[],           # Liste vide au départ
            state="readonly",    # L'utilisateur ne peut choisir que dans la liste
            width=30,
        )
        self.liste_indicateur.pack()

        # Label pour choisir la date de début
        ttk.Label(
            self.form_frame,
            text="Date de debut:",
            style="Texte.TLabel",
        ).pack(pady=(15, 5))

        # Variable stockant la date de début
        self.start_date_var = tk.StringVar()

        # Liste déroulante des dates de début
        self.liste_date_debut = ttk.Combobox(
            self.form_frame,
            textvariable=self.start_date_var,
            values=[],
            state="readonly",
            width=30,
        )
        self.liste_date_debut.pack()

        # Label pour choisir la date de fin
        ttk.Label(
            self.form_frame,
            text="Date de fin:",
            style="Texte.TLabel",
        ).pack(pady=(15, 5))

        # Variable stockant la date de fin
        self.end_date_var = tk.StringVar()

        # Liste déroulante des dates de fin
        self.liste_date_fin = ttk.Combobox(
            self.form_frame,
            textvariable=self.end_date_var,
            values=[],
            state="readonly",
            width=30,
        )
        self.liste_date_fin.pack()

        # -------------------------
        # Panneau de droite : graphique
        # -------------------------

        # Frame qui contiendra le graphique
        self.graph_frame = tk.Frame(self.content_frame, bg="#f4f6f8")

        # Placement dans la grille
        self.graph_frame.grid(row=0, column=1, sticky="nsew", padx=(30, 0))

        # Configuration de la grille du graphique
        self.graph_frame.grid_rowconfigure(0, weight=1)
        self.graph_frame.grid_columnconfigure(0, weight=1)

        # Création de la figure matplotlib
        self.figure = Figure(figsize=(6, 4), dpi=100)

        # Ajout d'un axe pour tracer le graphique
        self.ax = self.figure.add_subplot(111)

        # Création du canvas pour afficher la figure dans tkinter
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.graph_frame)

        # Placement du graphique dans la grille
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")

    # Méthode permettant d'associer une fonction lorsque l'utilisateur change une sélection
    def set_on_selection_change(self, callback):

        # Déclenche le callback lorsqu'un indicateur est sélectionné
        self.liste_indicateur.bind("<<ComboboxSelected>>", lambda _e: callback())

        # Déclenche le callback lorsque la date de début change
        self.liste_date_debut.bind("<<ComboboxSelected>>", lambda _e: callback())

        # Déclenche le callback lorsque la date de fin change
        self.liste_date_fin.bind("<<ComboboxSelected>>", lambda _e: callback())

    # Méthode pour définir la liste des indicateurs disponibles
    def set_indicateurs(self, indicateurs):
        self.liste_indicateur["values"] = indicateurs

        # Sélection automatique du premier indicateur s'il existe
        if indicateurs:
            self.indicateur_var.set(indicateurs[0])
        else:
            self.indicateur_var.set("")

    # Méthode pour définir les dates disponibles
    def set_dates(self, dates):

        # Remplissage des deux listes déroulantes
        self.liste_date_debut["values"] = dates
        self.liste_date_fin["values"] = dates

        # Sélection automatique de la première et dernière date
        if dates:
            self.start_date_var.set(dates[0])
            self.end_date_var.set(dates[-1])
        else:
            self.start_date_var.set("")
            self.end_date_var.set("")

    # Retourne l'indicateur sélectionné
    def get_indicateur_label(self):
        return self.indicateur_var.get().strip()

    # Retourne la date de début sélectionnée
    def get_date_debut(self):
        return self.start_date_var.get().strip()

    # Retourne la date de fin sélectionnée
    def get_date_fin(self):
        return self.end_date_var.get().strip()

    # Retourne l'objet axe matplotlib pour tracer le graphique
    def get_plot_axes(self):
        return self.ax

    # Redessine le graphique après modification
    def redraw_plot(self):
        self.canvas.draw()

    # Efface le graphique
    def clear_plot(self, message=None):

        # Supprime tout ce qui est affiché
        self.ax.clear()

        # Si un message est fourni, il est affiché au centre du graphique
        if message:
            self.ax.text(
                0.5,
                0.5,
                message,
                ha="center",
                va="center",
                transform=self.ax.transAxes,
            )

            # Cache les axes
            self.ax.set_axis_off()

        # Mise à jour de l'affichage
        self.canvas.draw()