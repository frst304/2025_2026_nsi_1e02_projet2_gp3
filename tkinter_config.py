import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

from Compare_region import comparer_regions, _strip_accents


def creer_fenetre(donnees, region_col):
    fenetre = tk.Tk()
    fenetre.title("Projet python")
    fenetre.geometry("1000x600")
    fenetre.configure(bg="#f4f6f8")

    style = ttk.Style()
    try:
        style.theme_use("clam")
    except tk.TclError:
        pass
    style.configure(
        "TCombobox",
        padding=6,
    )
    style.configure(
        "Titre.TLabel",
        font=("Segoe UI", 18, "bold"),
        background="#f4f6f8",
        foreground="#1f2a44",
    )
    style.configure(
        "Texte.TLabel",
        font=("Segoe UI", 11),
        background="#f4f6f8",
        foreground="#2d3b55",
    )
    style.configure(
        "Nav.TButton",
        font=("Segoe UI", 10, "bold"),
        padding=8,
    )
    style.configure(
        "Action.TButton",
        font=("Segoe UI", 11, "bold"),
        padding=8,
    )

    nav_bar = tk.Frame(fenetre, bg="#1f2a44")
    nav_bar.pack(fill="x")

    contenu = tk.Frame(fenetre, bg="#f4f6f8")
    contenu.pack(fill="both", expand=True)

    page_home = tk.Frame(contenu, bg="#f4f6f8")
    page_compare = tk.Frame(contenu, bg="#f4f6f8")

    for page in (page_home, page_compare):
        page.grid(row=0, column=0, sticky="nsew")

    def afficher_page(page):
        page.tkraise()

    bouton_home = tk.Button(
        nav_bar,
        text="Home",
        command=lambda: afficher_page(page_home),
        width=12,
        bg="#1f2a44",
        fg="#ffffff",
        activebackground="#2b3a5c",
        activeforeground="#ffffff",
        relief="flat",
    )
    bouton_home.pack(side="left", padx=5, pady=5)

    bouton_compare = tk.Button(
        nav_bar,
        text="Comparer par regions",
        command=lambda: afficher_page(page_compare),
        width=20,
        bg="#1f2a44",
        fg="#ffffff",
        activebackground="#2b3a5c",
        activeforeground="#ffffff",
        relief="flat",
    )
    bouton_compare.pack(side="left", padx=5, pady=5)

    def _regions_disponibles():
        if not region_col:
            return []
        regions = (
            donnees[region_col]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )
        regions = sorted(_strip_accents(r) for r in regions)
        return regions

    titre_compare = ttk.Label(
        page_compare,
        text="Comparer les regions",
        style="Titre.TLabel",
    )
    titre_compare.pack(pady=20)

    regions = _regions_disponibles()
    if not regions:
        messagebox.showerror(
            "Erreur",
            "Aucune colonne de region detectee dans les donnees.",
        )
    region_1_var = tk.StringVar(value=regions[0] if regions else "")
    region_2_var = tk.StringVar(value=regions[1] if len(regions) > 1 else "")

    form_frame = tk.Frame(page_compare, bg="#f4f6f8")
    form_frame.pack(pady=10)

    label_1 = ttk.Label(form_frame, text="Region 1:", style="Texte.TLabel")
    label_1.pack(pady=(10, 5))
    liste_1 = ttk.Combobox(
        form_frame,
        textvariable=region_1_var,
        values=regions,
        state="readonly",
        width=37,
    )
    liste_1.pack()

    label_2 = ttk.Label(form_frame, text="Region 2:", style="Texte.TLabel")
    label_2.pack(pady=(15, 5))
    liste_2 = ttk.Combobox(
        form_frame,
        textvariable=region_2_var,
        values=regions,
        state="readonly",
        width=37,
    )
    liste_2.pack()

    indicateurs = [
        ("Hospitalisations (nouvelles)", "incid_hosp"),
        ("Reanimations (nouvelles)", "incid_rea"),
        ("Deces hopital (nouveaux)", "incid_dchosp"),
        ("Hospitalises (actuels)", "hosp"),
        ("Reanimations (actuels)", "rea"),
        ("Deces hopital (cumul)", "dchosp"),
    ]
    indicateurs_disponibles = [
        (label, col)
        for label, col in indicateurs
        if col in donnees.columns
    ]
    indicateur_labels = [label for label, _ in indicateurs_disponibles]
    indicateur_var = tk.StringVar(
        value=indicateur_labels[0] if indicateur_labels else ""
    )

    label_indicateur = ttk.Label(
        form_frame, text="Indicateur:", style="Texte.TLabel"
    )
    label_indicateur.pack(pady=(15, 5))
    liste_indicateur = ttk.Combobox(
        form_frame,
        textvariable=indicateur_var,
        values=indicateur_labels,
        state="readonly",
        width=37,
    )
    liste_indicateur.pack()

    def lancer_comparaison():
        if not region_col:
            messagebox.showerror(
                "Erreur",
                "Aucune colonne de region detectee dans les donnees.",
            )
            return
        region_1 = region_1_var.get().strip()
        region_2 = region_2_var.get().strip()
        if not region_1 or not region_2:
            messagebox.showwarning(
                "Saisie incomplete",
                "Veuillez choisir deux regions.",
            )
            return
        indicateur_label = indicateur_var.get().strip()
        indicateur_col = None
        for label, col in indicateurs_disponibles:
            if label == indicateur_label:
                indicateur_col = col
                break
        if not indicateur_col:
            messagebox.showwarning(
                "Indicateur manquant",
                "Veuillez choisir un indicateur valide.",
            )
            return
        try:
            comparer_regions(
                donnees,
                [region_1, region_2],
                region_col=region_col,
                value_col=indicateur_col,
                value_label=indicateur_label,
            )
        except ValueError as exc:
            messagebox.showerror("Erreur", str(exc))

    bouton_lancer = tk.Button(
        form_frame,
        text="Comparer",
        command=lancer_comparaison,
        width=18,
        bg="#2f6fed",
        fg="#ffffff",
        activebackground="#3c7bff",
        activeforeground="#ffffff",
        relief="flat",
    )
    bouton_lancer.pack(pady=20)

    titre_home = ttk.Label(
        page_home,
        text="Accueil",
        style="Titre.TLabel",
    )
    titre_home.pack(pady=30)

    afficher_page(page_home)

    return fenetre