import tkinter as tk
from tkinter import ttk

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


class CompareRegionView:

    def __init__(self, parent, on_compare_callback=None, **kwargs):
        self.frame = tk.Frame(parent, bg="#f4f6f8", **kwargs)
        self.on_compare_callback = on_compare_callback
        self._build_ui()

    def _build_ui(self):
        self.titre = ttk.Label(
            self.frame,
            text="Comparer les regions",
            style="Titre.TLabel",
        )
        self.titre.pack(pady=20)

        self.content_frame = tk.Frame(self.frame, bg="#f4f6f8")
        self.content_frame.pack(fill="both", expand=True, padx=20, pady=10)
        self.content_frame.grid_columnconfigure(0, weight=0)
        self.content_frame.grid_columnconfigure(1, weight=1)
        self.content_frame.grid_rowconfigure(0, weight=1)

        self.form_frame = tk.Frame(self.content_frame, bg="#f4f6f8")
        self.form_frame.grid(row=0, column=0, sticky="nw")

        ttk.Label(self.form_frame, text="Region 1:", style="Texte.TLabel").pack(
            pady=(10, 5)
        )
        self.region_1_var = tk.StringVar()
        self.liste_region_1 = ttk.Combobox(
            self.form_frame,
            textvariable=self.region_1_var,
            values=[],
            state="readonly",
            width=37,
        )
        self.liste_region_1.pack()

        ttk.Label(self.form_frame, text="Region 2:", style="Texte.TLabel").pack(
            pady=(15, 5)
        )
        self.region_2_var = tk.StringVar()
        self.liste_region_2 = ttk.Combobox(
            self.form_frame,
            textvariable=self.region_2_var,
            values=[],
            state="readonly",
            width=37,
        )
        self.liste_region_2.pack()

        ttk.Label(self.form_frame, text="Indicateur:", style="Texte.TLabel").pack(
            pady=(15, 5)
        )
        self.indicateur_var = tk.StringVar()
        self.liste_indicateur = ttk.Combobox(
            self.form_frame,
            textvariable=self.indicateur_var,
            values=[],
            state="readonly",
            width=37,
        )
        self.liste_indicateur.pack()

        self.bouton_lancer = tk.Button(
            self.form_frame,
            text="Comparer",
            command=self._on_compare_click,
            width=18,
            bg="#2f6fed",
            fg="#ffffff",
            activebackground="#3c7bff",
            activeforeground="#ffffff",
            relief="flat",
        )
        self.bouton_lancer.pack(pady=20)

        self.graph_frame = tk.Frame(self.content_frame, bg="#f4f6f8")
        self.graph_frame.grid(row=0, column=1, sticky="nsew", padx=(30, 0))
        self.graph_frame.grid_rowconfigure(0, weight=1)
        self.graph_frame.grid_columnconfigure(0, weight=1)

        self.figure = Figure(figsize=(6, 4), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.graph_frame)
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")

    def _on_compare_click(self):
        if self.on_compare_callback:
            self.on_compare_callback()

    def set_on_selection_change(self, callback):
        self.liste_region_1.bind("<<ComboboxSelected>>", lambda _e: callback())
        self.liste_region_2.bind("<<ComboboxSelected>>", lambda _e: callback())
        self.liste_indicateur.bind("<<ComboboxSelected>>", lambda _e: callback())

    def set_regions(self, regions):
        self.liste_region_1["values"] = regions
        self.liste_region_2["values"] = regions
        if regions:
            self.region_1_var.set(regions[0])
        if len(regions) > 1:
            self.region_2_var.set(regions[1])

    def set_indicateurs(self, indicateur_labels):
        self.liste_indicateur["values"] = indicateur_labels
        if indicateur_labels:
            self.indicateur_var.set(indicateur_labels[0])

    def get_region_1(self):
        return self.region_1_var.get().strip()

    def get_region_2(self):
        return self.region_2_var.get().strip()

    def get_indicateur_label(self):
        return self.indicateur_var.get().strip()

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

    def set_on_compare_callback(self, callback):
        self.on_compare_callback = callback
