import tkinter as tk
from tkinter import ttk

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


class FranceView:

    def __init__(self, parent, **kwargs):
        self.frame = tk.Frame(parent, bg="#f4f6f8", **kwargs)
        self._build_ui()

    def _build_ui(self):
        self.titre = ttk.Label(
            self.frame,
            text="France entiere",
            style="Titre.TLabel",
        )
        self.titre.pack(pady=20)

        self.content_frame = tk.Frame(self.frame, bg="#f4f6f8")
        self.content_frame.pack(fill="both", expand=True, padx=20, pady=10)
        self.content_frame.grid_columnconfigure(0, weight=0)
        self.content_frame.grid_columnconfigure(1, weight=1)
        self.content_frame.grid_rowconfigure(0, weight=1)

        # Panneau de gauche : choix de l'indicateur
        self.form_frame = tk.Frame(self.content_frame, bg="#f4f6f8")
        self.form_frame.grid(row=0, column=0, sticky="nw")

        ttk.Label(self.form_frame, text="Indicateur:", style="Texte.TLabel").pack(
            pady=(10, 5)
        )
        self.indicateur_var = tk.StringVar()
        self.liste_indicateur = ttk.Combobox(
            self.form_frame,
            textvariable=self.indicateur_var,
            values=[],
            state="readonly",
            width=30,
        )
        self.liste_indicateur.pack()

        ttk.Label(
            self.form_frame,
            text="Date de debut:",
            style="Texte.TLabel",
        ).pack(pady=(15, 5))
        self.start_date_var = tk.StringVar()
        self.liste_date_debut = ttk.Combobox(
            self.form_frame,
            textvariable=self.start_date_var,
            values=[],
            state="readonly",
            width=30,
        )
        self.liste_date_debut.pack()

        ttk.Label(
            self.form_frame,
            text="Date de fin:",
            style="Texte.TLabel",
        ).pack(pady=(15, 5))
        self.end_date_var = tk.StringVar()
        self.liste_date_fin = ttk.Combobox(
            self.form_frame,
            textvariable=self.end_date_var,
            values=[],
            state="readonly",
            width=30,
        )
        self.liste_date_fin.pack()

        # Panneau de droite : graphique
        self.graph_frame = tk.Frame(self.content_frame, bg="#f4f6f8")
        self.graph_frame.grid(row=0, column=1, sticky="nsew", padx=(30, 0))
        self.graph_frame.grid_rowconfigure(0, weight=1)
        self.graph_frame.grid_columnconfigure(0, weight=1)

        self.figure = Figure(figsize=(6, 4), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.graph_frame)
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")

    def set_on_selection_change(self, callback):
        self.liste_indicateur.bind("<<ComboboxSelected>>", lambda _e: callback())
        self.liste_date_debut.bind("<<ComboboxSelected>>", lambda _e: callback())
        self.liste_date_fin.bind("<<ComboboxSelected>>", lambda _e: callback())

    def set_indicateurs(self, indicateurs):
        self.liste_indicateur["values"] = indicateurs
        if indicateurs:
            self.indicateur_var.set(indicateurs[0])
        else:
            self.indicateur_var.set("")

    def set_dates(self, dates):
        self.liste_date_debut["values"] = dates
        self.liste_date_fin["values"] = dates
        if dates:
            self.start_date_var.set(dates[0])
            self.end_date_var.set(dates[-1])
        else:
            self.start_date_var.set("")
            self.end_date_var.set("")

    def get_indicateur_label(self):
        return self.indicateur_var.get().strip()

    def get_date_debut(self):
        return self.start_date_var.get().strip()

    def get_date_fin(self):
        return self.end_date_var.get().strip()

    def get_plot_axes(self):
        return self.ax

    def redraw_plot(self):
        self.canvas.draw()

    def clear_plot(self, message=None):
        self.ax.clear()
        if message:
            self.ax.text(
                0.5,
                0.5,
                message,
                ha="center",
                va="center",
                transform=self.ax.transAxes,
            )
            self.ax.set_axis_off()
        self.canvas.draw()

