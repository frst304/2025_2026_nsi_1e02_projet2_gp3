# Import de la bibliothèque tkinter pour l'interface graphique
import tkinter as tk

# Import des widgets ttk (versions améliorées de tkinter)
from tkinter import ttk

# Import du module permettant d'intégrer matplotlib dans tkinter
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Import de l'objet Figure de matplotlib pour créer des graphiques
from matplotlib.figure import Figure


# Classe représentant la vue permettant de comparer les régions
class CompareRegionView:

    # Constructeur de la classe
    def __init__(self, parent, on_compare_callback=None, **kwargs):

        # Création du frame principal de la page
        self.frame = tk.Frame(parent, bg="#f4f6f8", **kwargs)

        # Fonction callback optionnelle appelée lors d'une comparaison
        self.on_compare_callback = on_compare_callback

        # Construction de l'interface graphique
        self._build_ui()

    # Méthode privée qui construit l'interface utilisateur
    def _build_ui(self):

        # Création du titre de la page
        self.titre = ttk.Label(
            self.frame,
            text="Comparer les regions",
            style="Titre.TLabel",
        )

        # Placement du titre
        self.titre.pack(pady=20)

        # Frame principal contenant les contrôles et le graphique
        self.content_frame = tk.Frame(self.frame, bg="#f4f6f8")
        self.content_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Configuration de la grille
        self.content_frame.grid_columnconfigure(0, weight=0)
        self.content_frame.grid_columnconfigure(1, weight=1)
        self.content_frame.grid_rowconfigure(0, weight=1)

        # -------------------------
        # Panneau de gauche : formulaire de sélection
        # -------------------------

        # Frame contenant les contrôles
        self.form_frame = tk.Frame(self.content_frame, bg="#f4f6f8")
        self.form_frame.grid(row=0, column=0, sticky="nw")

        # Label pour choisir la première région
        ttk.Label(self.form_frame, text="Region 1:", style="Texte.TLabel").pack(
            pady=(10, 5)
        )

        # Variable stockant la région 1
        self.region_1_var = tk.StringVar()

        # Liste déroulante des régions
        self.liste_region_1 = ttk.Combobox(
            self.form_frame,
            textvariable=self.region_1_var,
            values=[],
            state="readonly",
            width=37,
        )
        self.liste_region_1.pack()

        # Label pour choisir la deuxième région
        ttk.Label(self.form_frame, text="Region 2:", style="Texte.TLabel").pack(
            pady=(15, 5)
        )

        # Variable stockant la région 2
        self.region_2_var = tk.StringVar()

        # Liste déroulante des régions
        self.liste_region_2 = ttk.Combobox(
            self.form_frame,
            textvariable=self.region_2_var,
            values=[],
            state="readonly",
            width=37,
        )
        self.liste_region_2.pack()

        # Label pour choisir l'indicateur
        ttk.Label(self.form_frame, text="Indicateur:", style="Texte.TLabel").pack(
            pady=(15, 5)
        )

        # Variable stockant l'indicateur sélectionné
        self.indicateur_var = tk.StringVar()

        # Liste déroulante des indicateurs
        self.liste_indicateur = ttk.Combobox(
            self.form_frame,
            textvariable=self.indicateur_var,
            values=[],
            state="readonly",
            width=37,
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
            width=37,
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
            width=37,
        )
        self.liste_date_fin.pack()

        # -------------------------
        # Panneau de droite : graphique
        # -------------------------

        # Frame qui contiendra le graphique
        self.graph_frame = tk.Frame(self.content_frame, bg="#f4f6f8")
        self.graph_frame.grid(row=0, column=1, sticky="nsew", padx=(30, 0))

        # Configuration de la grille
        self.graph_frame.grid_rowconfigure(0, weight=1)
        self.graph_frame.grid_columnconfigure(0, weight=1)

        # Création de la figure matplotlib
        self.figure = Figure(figsize=(6, 4), dpi=100)

        # Création d'un axe pour dessiner le graphique
        self.ax = self.figure.add_subplot(111)

        # Création du canvas pour afficher matplotlib dans tkinter
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.graph_frame)

        # Placement du graphique dans la grille
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")

    # Méthode pour déclencher un callback lorsqu'une sélection change
    def set_on_selection_change(self, callback):
        self.liste_region_1.bind("<<ComboboxSelected>>", lambda _e: callback())
        self.liste_region_2.bind("<<ComboboxSelected>>", lambda _e: callback())
        self.liste_indicateur.bind("<<ComboboxSelected>>", lambda _e: callback())
        self.liste_date_debut.bind("<<ComboboxSelected>>", lambda _e: callback())
        self.liste_date_fin.bind("<<ComboboxSelected>>", lambda _e: callback())

    # Méthode pour définir la liste des régions disponibles
    def set_regions(self, regions):
        self.liste_region_1["values"] = regions
        self.liste_region_2["values"] = regions
        self.region_1_var.set("")
        self.region_2_var.set("")

    # Méthode pour définir les indicateurs disponibles
    def set_indicateurs(self, indicateur_labels):
        self.liste_indicateur["values"] = indicateur_labels
        self.indicateur_var.set("")

    # Méthode pour définir les dates disponibles
    def set_dates(self, dates):
        """
        Initialise les listes déroulantes avec les dates disponibles.
        """
        self.liste_date_debut["values"] = dates
        self.liste_date_fin["values"] = dates

        if dates:
            # Par défaut on sélectionne toute la période disponible
            self.start_date_var.set(dates[0])
            self.end_date_var.set(dates[-1])
        else:
            self.start_date_var.set("")
            self.end_date_var.set("")

    # Retourne la région 1 sélectionnée
    def get_region_1(self):
        return self.region_1_var.get().strip()

    # Retourne la région 2 sélectionnée
    def get_region_2(self):
        return self.region_2_var.get().strip()

    # Retourne l'indicateur sélectionné
    def get_indicateur_label(self):
        return self.indicateur_var.get().strip()

    # Retourne la date de début sélectionnée
    def get_date_debut(self):
        return self.start_date_var.get().strip()

    # Retourne la date de fin sélectionnée
    def get_date_fin(self):
        return self.end_date_var.get().strip()

    # Retourne l'axe matplotlib pour tracer le graphique
    def get_plot_axes(self):
        return self.ax

    # Redessine le graphique
    def redraw_plot(self):
        self.canvas.draw()

    # Efface le graphique
    def clear_plot(self, message=None):

        # Supprime le contenu actuel
        self.ax.clear()

        # Si un message est fourni, il est affiché au centre
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

    # Permet de définir la fonction appelée lors de la comparaison
    def set_on_compare_callback(self, callback):
        self.on_compare_callback = callback