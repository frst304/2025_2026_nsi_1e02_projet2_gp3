import tkinter as tk
from tkinter import ttk


class FranceMapView:

    def __init__(self, parent, **kwargs):
        self.frame = tk.Frame(parent, bg="#f4f6f8", **kwargs)
        self._build_ui()

    def _build_ui(self):
        self.titre = ttk.Label(
            self.frame,
            text="Carte de France par departement",
            style="Titre.TLabel",
        )
        self.titre.pack(pady=20)

        self.content_frame = tk.Frame(self.frame, bg="#f4f6f8")
        self.content_frame.pack(fill="both", expand=True, padx=20, pady=10)

        self.form_frame = tk.Frame(self.content_frame, bg="#f4f6f8")
        self.form_frame.pack(anchor="nw")

        ttk.Label(self.form_frame, text="Indicateur:", style="Texte.TLabel").pack(
            pady=(10, 5)
        )
        self.indicateur_var = tk.StringVar()
        self.liste_indicateur = ttk.Combobox(
            self.form_frame,
            textvariable=self.indicateur_var,
            values=[],
            state="readonly",
            width=40,
        )
        self.liste_indicateur.pack()

        ttk.Label(self.form_frame, text="Date de debut:", style="Texte.TLabel").pack(
            pady=(15, 5)
        )
        self.start_date_var = tk.StringVar()
        self.liste_date_debut = ttk.Combobox(
            self.form_frame,
            textvariable=self.start_date_var,
            values=[],
            state="readonly",
            width=40,
        )
        self.liste_date_debut.pack()

        ttk.Label(self.form_frame, text="Date de fin:", style="Texte.TLabel").pack(
            pady=(15, 5)
        )
        self.end_date_var = tk.StringVar()
        self.liste_date_fin = ttk.Combobox(
            self.form_frame,
            textvariable=self.end_date_var,
            values=[],
            state="readonly",
            width=40,
        )
        self.liste_date_fin.pack()

        self.btn_generer = ttk.Button(
            self.form_frame,
            text="Generer la carte interactive",
        )
        self.btn_generer.pack(pady=20)

        self.label_info = ttk.Label(
            self.frame,
            text="La carte sera ouverte dans votre navigateur par defaut.",
            style="Texte.TLabel",
        )
        self.label_info.pack(pady=(0, 10))

    def set_indicateurs(self, indicateurs):
        self.liste_indicateur["values"] = indicateurs
        if indicateurs:
            self.indicateur_var.set(indicateurs[0])
        else:
            self.indicateur_var.set("")

    def set_dates(self, dates):
        self.liste_date_debut["values"] = dates
        self.liste_date_fin["values"] = dates
        self.start_date_var.set("")
        self.end_date_var.set("")

    def get_indicateur_label(self):
        return self.indicateur_var.get().strip()

    def get_date_debut(self):
        return self.start_date_var.get().strip()

    def get_date_fin(self):
        return self.end_date_var.get().strip()

    def set_on_generate(self, callback):
        self.btn_generer.config(command=callback)

