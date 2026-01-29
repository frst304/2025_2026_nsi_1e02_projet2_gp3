import tkinter as tk
from tkinter import ttk


class HomeView:

    def __init__(self, parent, **kwargs):
        self.frame = tk.Frame(parent, bg="#f4f6f8", **kwargs)
        self._build_ui()

    def _build_ui(self):
        self.titre = ttk.Label(
            self.frame,
            text="Accueil",
            style="Titre.TLabel",
        )
        self.titre.pack(pady=30)

        self.stats_frame = tk.Frame(self.frame, bg="#f4f6f8")
        self.stats_frame.pack(pady=10)

        self.label_hosp = ttk.Label(
            self.stats_frame,
            text="Hospitalisations (actuels): indisponible",
            style="Stats.TLabel",
        )
        self.label_hosp.pack(pady=5)

        self.label_deces = ttk.Label(
            self.stats_frame,
            text="Deces hopital (cumul): indisponible",
            style="Stats.TLabel",
        )
        self.label_deces.pack(pady=5)

    def set_stats(self, total_hosp=None, total_deces=None):
        if total_hosp is not None:
            self.label_hosp.config(
                text=f"Hospitalisations (actuels): {int(total_hosp):,}".replace(",", " ")
            )
        else:
            self.label_hosp.config(text="Hospitalisations (actuels): indisponible")

        if total_deces is not None:
            self.label_deces.config(
                text=f"Deces hopital (cumul): {int(total_deces):,}".replace(",", " ")
            )
        else:
            self.label_deces.config(text="Deces hopital (cumul): indisponible")
